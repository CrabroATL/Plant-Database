import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imshow
import psycopg2 as psy
import pytesseract
import PIL
import os
import json
import time

plt.switch_backend('TkAgg')

# global transform variables
x_transform = 780
y_middle_transform = 675
y_bottom_transform = 1346
text_crop_species = (150, 555, 790, 710)
text_crop_bools = (610, 420, 700, 550)
x_transform_tuple = (x_transform, 0, x_transform, 0)
y_middle_transform_tuple = (0, y_middle_transform, 0, y_middle_transform)
y_bottom_transform_tuple = (0, y_bottom_transform, 0, y_bottom_transform)
QUADRANT_COUNT = 6
GRAYSCALE_BLACK_VALUE = 0.5

def ocr_image(quadrant, text_crop_species, text_crop_bools, x_transform_tuple, y_middle_transform_tuple, y_bottom_transform_tuple, img):
    if quadrant == 0: 
        species_crop = img.crop(text_crop_species)
        bool_crop = img.crop(text_crop_bools)
    elif quadrant == 1:
        species_crop = img.crop(tuple(np.add(text_crop_species, x_transform_tuple)))
        bool_crop = img.crop(tuple(np.add(text_crop_bools, x_transform_tuple)))
    elif quadrant == 2:
        species_crop = img.crop(tuple(np.add(text_crop_species, y_middle_transform_tuple)))
        bool_crop = img.crop(tuple(np.add(text_crop_bools, y_middle_transform_tuple)))
    elif quadrant == 3:
        species_crop = img.crop(tuple(np.add((tuple(np.add(text_crop_species, y_middle_transform_tuple))), x_transform_tuple)))
        bool_crop = img.crop(tuple(np.add((tuple(np.add(text_crop_bools, y_middle_transform_tuple))), x_transform_tuple)))
    elif quadrant == 4:
        species_crop = img.crop(tuple(np.add(text_crop_species, y_bottom_transform_tuple)))
        bool_crop = img.crop(tuple(np.add(text_crop_bools, y_bottom_transform_tuple)))
    elif quadrant == 5:
        species_crop = img.crop(tuple(np.add((tuple(np.add(text_crop_species, y_bottom_transform_tuple))), x_transform_tuple)))
        bool_crop = img.crop(tuple(np.add((tuple(np.add(text_crop_bools, y_bottom_transform_tuple))), x_transform_tuple)))
    else:
        raise Exception("no quadrant error")
    
    np_species_crop = np.asarray(species_crop)
    np_bool_crop = np.asarray(bool_crop)
    ocr_start = time.time()
    raw_bool = pytesseract.image_to_string(np_bool_crop,config="--psm 6 digits")
    raw_text = pytesseract.image_to_string(np_species_crop)
    ocr_end = time.time()
    lined_text = raw_text.splitlines()
    clean_text = [line for line in lined_text if line != "" and line != " "]
    print(clean_text)
    ocr_time = (ocr_end - ocr_start)
    return(clean_text, raw_bool, ocr_time)

def set_bools(raw_bool):
    if "1" or "2" or "3" or "4" not in raw_bool:
        native_bool = True
        endemic_bool = False
        special_concern_bool = False
        introduced_bool = False
        invasive_bool = False
    if "1" in raw_bool:
        introduced_bool = True
        native_bool = False
        endemic_bool = False
        special_concern_bool = False
        invasive_bool = False
    if "2" in raw_bool:
        introduced_bool = False
        native_bool = True
        endemic_bool = True
        special_concern_bool = False
        invasive_bool = False
    if "3" in raw_bool:
        introduced_bool = True
        native_bool = False
        endemic_bool = False
        special_concern_bool = False
        invasive_bool = True
    if "4" in raw_bool:
        introduced_bool = False
        native_bool = True
        special_concern_bool = True
        invasive_bool = False
    return(native_bool, endemic_bool, special_concern_bool, introduced_bool, invasive_bool)

def process_images(cur, path, phyla):
    
    # y is before x when indexing into the image
    # TODO put counties into JSON file and read the JSON file into "counties"
    # maybe TODO create county class
    
    with open("countiesxy.json", "r") as file:
        counties = json.load(file)
    
    # quadrants are numbered left to right, top to bottom from 0 - 5
    transform_x = 0
    transform_y = 0
    loop_ocr_time = 0
    for quadrant in range(QUADRANT_COUNT):
        start_image_time = time.time()
        image = imread(path, as_gray = True)
        img = PIL.Image.open(path)
        end_image_time = time.time()
        image_time = end_image_time - start_image_time
        # extract text data based on quadrant
        clean_text, raw_bool, ocr_time = ocr_image(quadrant, text_crop_species, text_crop_bools, x_transform_tuple, y_middle_transform_tuple, y_bottom_transform_tuple, img)
        loop_ocr_time = loop_ocr_time + ocr_time
        if len(clean_text) == 0:
            break    
        native_bool, endemic_bool, special_concern_bool, introduced_bool, invasive_bool = set_bools(raw_bool)
        db_start = time.time()
        cur.execute("SELECT phyla_id FROM phyla WHERE polyphylactic_group = %s", (phyla,))
        phyla_id = cur.fetchone()[0]

        if "infraspecific" in clean_text[-1]:
            family = clean_text[0].replace(" ", "")
            genera = clean_text[1].split(" ")[0]
            species = "".join(clean_text[1:-2])
            common = clean_text[-2]
        else:
            family = clean_text[0].replace(" ", "")
            genera = clean_text[1].split(" ")[0]
            species = "".join(clean_text[1:-1])
            common = clean_text[-1]

        #lowercase data
        family = family.lower()
        genera = genera.lower()
        species = species.lower()
        common = common.lower()
        # Avoid duplicate insertions into database
        cur.execute("SELECT family_id FROM family WHERE family = %s", (family,))
        family_id_test = cur.fetchone()
        cur.execute("SELECT genera_id FROM genera WHERE genera = %s", (genera,))
        genera_id_test = cur.fetchone()
        cur.execute("SELECT species_id FROM species WHERE scientific_name = %s", (species,))
        species_id_test = cur.fetchone()

        if family_id_test == None:
            cur.execute("INSERT INTO family VALUES (DEFAULT, %s, %s)", (family, phyla_id))    
        cur.execute("SELECT family_id FROM family WHERE family = %s", (family,))
        family_id = cur.fetchone()[0]
        if genera_id_test == None:
            cur.execute("INSERT INTO genera VALUES (DEFAULT, %s, %s, %s)", (genera, family_id, phyla_id))
        cur.execute("SELECT genera_id FROM genera WHERE genera = %s", (genera,))
        genera_id = cur.fetchone()[0]
        if species_id_test == None:
            cur.execute("INSERT INTO species VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (species, common, native_bool, endemic_bool, special_concern_bool, introduced_bool, invasive_bool, genera_id, family_id, phyla_id))
        else:
            continue
        
        # x transform conditions
        if quadrant % 2 != 0:
            transform_x = x_transform
            transform_y = 0
        else:
            transform_x = 0
            transform_y = 0
        # y transform conditions
        if quadrant in [2, 3]:
            transform_y = y_middle_transform
        elif quadrant in [4, 5]:
            transform_y = y_bottom_transform 
        
        for county in counties:
            county_occurance = image[county["y"] + transform_y][county["x"] + transform_x]
            if county_occurance < GRAYSCALE_BLACK_VALUE:
                cur.execute("SELECT species_id FROM species WHERE scientific_name = %s;", (species,))
                species_id = cur.fetchone()
                cur.execute("SELECT county_id FROM counties WHERE county_name = %s;", (county["name"],))
                county_id = cur.fetchone()
                cur.execute("INSERT INTO county_occurance VALUES (%s, %s);", (species_id, county_id,))
                continue
        db_end = time.time()
        db_time = (db_end - db_start)
    return(loop_ocr_time, db_time, image_time)
                
def main():
    start = time.time()
    conn = psy.connect('dbname=postgres user=postgres password=password host=0.0.0.0 port=30420')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SET search_path TO ar_plants;")

    # gather county data    
    total_ocr_time = 0
    total_db_time = 0
    total_image_time = 0
    for file in os.listdir('images/'):
        path = "images/" + file
        phyla_name = (file.rsplit("_", 1)[0]).replace("_", " ")
        ocr_time, db_time, image_time = process_images(cur, path, phyla_name)
        total_ocr_time = total_ocr_time + ocr_time
        total_db_time = total_db_time + db_time
        total_image_time = total_image_time + image_time
        # upload_to_database(data) "maybe I wont build this function"
    end = time.time()
    print(end-start)
    print(total_ocr_time)
    print(total_db_time)
    print(total_image_time)

    # print(genera)

    # use config="--psm 6 digits" for retrieving numbers
    # print(pytesseract.image_to_string(q0, config="--psm 6 digits"))

    # imshow(q1)
    # plt.show()

    
main()



# problems for extracting scientific and common names.
# handle species with "infraspecific taxa and species status"
# if 5 lines of text, the middle three are the full scientific name
# some plants don't have a common name