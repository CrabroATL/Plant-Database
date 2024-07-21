import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imshow
import psycopg2 as psy
import pytesseract
import PIL
from os.path import exists

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

def transform_image():
    return

def process_images(cur, path, phyla):
    
    # y is before x when indexing into the image
    # TODO put counties into JSON file and read the JSON file into "counties"
    # maybe TODO create county class
    counties = [
        {"name": "arkansas",
        "x": 556,
        "y": 381
        },
        {"name": "ashley",
        "x": 516,
        "y": 526
        },
        {"name": "baxter",
        "x": 454,
        "y": 122
        },
        {"name": "benton",
            "x": 256,
            "y": 122
        },
        {"name": "boone",
            "x": 377,
            "y": 128
        },
        {"name": "bardley",
            "x": 473,
            "y": 490
        },
        {"name": "calhoun",
            "x": 438,
            "y": 480
        },
        {"name": "carroll",
            "x": 331,
            "y": 122
        },
        {"name": "chicot",
            "x": 565,
            "y": 514
        },
        {"name": "clark",
            "x": 368,
            "y": 418
        },
        {"name": "clay",
            "x": 651,
            "y": 113
        },
        {"name": "cleburne",
            "x": 484,
            "y": 225
        },
        {"name": "cleveland",
            "x": 474,
            "y": 436
        },
        {"name": "columbia",
            "x": 362,
            "y": 525
        },
        {"name": "conway",
            "x": 418,
            "y": 261
        },
        {"name": "craighead",
            "x": 633,
            "y": 186
        },
        {"name": "crawford",
            "x": 254,
            "y": 219
        },
        {"name": "crittenden",
            "x": 664,
            "y": 255
        },
        {"name": "cross",
            "x": 620,
            "y": 255
        },
        {"name": "dallas",
            "x": 421,
            "y": 428
        },
        {"name": "desha",
            "x": 566,
            "y": 447
        },
        {"name": "drew",
            "x": 521,
            "y": 475
        },
        {"name": "faulkner",
            "x": 455,
            "y": 278
        },
        {"name": "franklin",
            "x": 296,
            "y": 225
        },
        {"name": "fulton",
            "x": 505,
            "y": 116
        },
        {"name": "garland",
            "x": 368,
            "y": 351
        },
        {"name": "grant",
            "x": 443,
            "y": 388
        },
        {"name": "greene",
            "x": 636,
            "y": 150
        },
        {"name": "hempstead",
            "x": 316,
            "y": 456
        },
        {"name": "hotspring",
            "x": 399,
            "y": 386
        },
        {"name": "howard",
            "x": 285,
            "y": 414
        },
        {"name": "independence",
            "x": 532,
            "y": 202
        },
        {"name": "izard",
            "x": 499,
            "y": 155
        },
        {"name": "jackson",
            "x": 574,
            "y": 219
        },
        {"name": "jefferson",
            "x": 494,
            "y": 383
        },
        {"name": "johnson",
            "x": 335,
            "y": 222
        },
        {"name": "lafayette",
            "x": 321,
            "y": 525
        },
        {"name": "lawrence",
            "x": 583,
            "y": 163
        },
        {"name": "lee",
            "x": 619,
            "y": 322
        },
        {"name": "lincoln",
            "x": 519,
            "y": 430
        },
        {"name": "littleriver",
            "x": 249,
            "y": 462
        },
        {"name": "logan",
            "x": 312,
            "y": 263
        },
        {"name": "lonoke",
            "x": 504,
            "y": 325
        },
        {"name": "madison",
            "x": 310,
            "y": 170
        },
        {"name": "marion",
            "x": 415,
            "y": 134
        },
        {"name": "miller",
            "x": 290,
            "y": 509
        },
        {"name": "mississippi",
            "x": 686,
            "y": 189
        },
        {"name": "monroe",
            "x": 574,
            "y": 333
        },
        {"name": "montgomery",
            "x": 316,
            "y": 355
        },
        {"name": "nevada",
            "x": 354,
            "y": 468
        },
        {"name": "newton",
            "x": 377,
            "y": 128
        },
        {"name": "ouachita",
            "x": 393,
            "y": 475
        },
        {"name": "perry",
            "x": 395,
            "y": 300
        },
        {"name": "phillips",
            "x": 616,
            "y": 358
        },
        {"name": "pike",
            "x": 316,
            "y": 402
        },
        {"name": "poinsett",
            "x": 626,
            "y": 219
        },
        {"name": "polk",
            "x": 258,
            "y": 358
        },
        {"name": "pope",
            "x": 379,
            "y": 241
        },
        {"name": "prairie",
            "x": 538,
            "y": 316
        },
        {"name": "pulaski",
            "x": 460,
            "y": 325
        },
        {"name": "randolph",
            "x": 591,
            "y": 120
        },
        {"name": "saintfrancis",
            "x": 619,
            "y": 288
        },
        {"name": "saline",
            "x": 418,
            "y": 341
        },
        {"name": "scott",
            "x": 276,
            "y": 313
        },
        {"name": "searcy",
            "x": 416,
            "y": 178
        },
        {"name": "sebastian",
            "x": 251,
            "y": 265
        },
        {"name": "sevier",
            "x": 251,
            "y": 420
        },
        {"name": "sharp",
            "x": 538,
            "y": 152
        },
        {"name": "stone",
            "x": 465,
            "y": 185
        },
        {"name": "union",
            "x": 426,
            "y": 531
        },
        {"name": "vanburen",
            "x": 438,
            "y": 219
        },
        {"name": "washington",
            "x": 260,
            "y": 170
        },
        {"name": "white",
            "x": 516,
            "y": 264
        },
        {"name": "woodruff",
            "x": 572,
            "y": 269
        },
        {"name": "yell",
            "x": 338,
            "y": 294
        },
    ]

    # quadrants are numbered right to left, top to bottom from 0 - 5
    transform_x = 0
    transform_y = 0
    for quadrant in range(QUADRANT_COUNT):
        image = imread(path, as_gray = True)
        img = PIL.Image.open(path)
        
        # extract text data based on quadrant
        if quadrant == 0:
            quadrant0 = img.crop(text_crop_species)
            quadrant0_bool = img.crop(text_crop_bools)
            q0 = np.asarray(quadrant0)
            q_bool0 = np.asarray(quadrant0_bool)
            raw_text_bool0 = pytesseract.image_to_string(q_bool0,config="--psm 6 digits")
            raw_text0 = pytesseract.image_to_string(q0)
            lines_text0 = raw_text0.splitlines()       
        elif quadrant == 1:
            quadrant1 = img.crop(tuple(np.add(text_crop_species, x_transform_tuple)))
            quadrant1_bool = img.crop(tuple(np.add(text_crop_bools, x_transform_tuple)))
            q1 = np.asarray(quadrant1)
            q_bool1 = np.asarray(quadrant1_bool)
            raw_text_bool1 = pytesseract.image_to_string(q_bool1,config="--psm 6 digits")
            raw_text1 = pytesseract.image_to_string(q1)
            lines_text1 = raw_text1.splitlines()
        elif quadrant == 2:
            quadrant2 = img.crop(tuple(np.add(text_crop_species, y_middle_transform_tuple)))
            quadrant2_bool = img.crop(tuple(np.add(text_crop_bools, y_middle_transform_tuple)))
            q2 = np.asarray(quadrant2)
            q_bool2 = np.asarray(quadrant2_bool)
            raw_text_bool2 = pytesseract.image_to_string(q_bool2,config="--psm 6 digits")
            raw_text2 = pytesseract.image_to_string(q2)
            lines_text2 = raw_text2.splitlines()
        elif quadrant == 3:
            quadrant3 = img.crop(tuple(np.add((tuple(np.add(text_crop_species, y_middle_transform_tuple))), x_transform_tuple)))
            quadrant3_bool = img.crop(tuple(np.add((tuple(np.add(text_crop_bools, y_middle_transform_tuple))), x_transform_tuple)))
            q3 = np.asarray(quadrant3)
            q_bool3 = np.asarray(quadrant3_bool)
            raw_text_bool3 = pytesseract.image_to_string(q_bool3,config="--psm 6 digits")
            raw_text3 = pytesseract.image_to_string(q3)
            lines_text3 = raw_text3.splitlines()   
        elif quadrant == 4:
            quadrant4 = img.crop(tuple(np.add(text_crop_species, y_bottom_transform_tuple)))
            quadrant4_bool = img.crop(tuple(np.add(text_crop_bools, y_bottom_transform_tuple)))
            q4 = np.asarray(quadrant4)
            q_bool4 = np.asarray(quadrant4_bool)
            raw_text_bool4 = pytesseract.image_to_string(q_bool4, config="--psm 6 digits")
            raw_text4 = pytesseract.image_to_string(q4)
            lines_text4 = raw_text4.splitlines()
        elif quadrant == 5:
            quadrant5 = img.crop(tuple(np.add((tuple(np.add(text_crop_species, y_bottom_transform_tuple))), x_transform_tuple)))
            quadrant5_bool = img.crop(tuple(np.add((tuple(np.add(text_crop_bools, y_bottom_transform_tuple))), x_transform_tuple)))
            q5 = np.asarray(quadrant5)
            q_bool5 = np.asarray(quadrant5_bool)
            raw_text_bool5 = pytesseract.image_to_string(q_bool5, config="--psm 6 digits")
            raw_text5 = pytesseract.image_to_string(q5)
            lines_text5 = raw_text5.splitlines()
        else:
            raise Exception("no quadrant error")
        
        # check if quadrant is empty
        print(eval(("lines_text" + str(quadrant)))[0])
        if eval(("lines_text" + str(quadrant)))[0].isalnum() == False:
            continue
        
        # extract data into variables
        cur.execute("SELECT phyla_id FROM phyla WHERE polyphylactic_group = %s", (phyla,))
        phyla_id = cur.fetchone()[0]
        current_status = eval(("raw_text_bool" + str(quadrant)))
        if not ("1" or "2" or "3" or "4") in current_status:
            native_bool = True
            endemic_bool = False
            special_concern_bool = False
            introduced_bool = False
            invasive_bool = False
        if "1" in current_status:
            introduced_bool = True
            native_bool = False
            endemic_bool = False
            special_concern_bool = False
            invasive_bool = False
        if "2" in current_status:
            introduced_bool = False
            native_bool = True
            endemic_bool = True
            special_concern_bool = False
            invasive_bool = False
        if "3" in current_status:
            introduced_bool = True
            native_bool = False
            endemic_bool = False
            special_concern_bool = False
            invasive_bool = True
        if "4" in current_status:
            introduced_bool = False
            native_bool = True
            special_concern_bool = True
            invasive_bool = False
        
        # rules of text extraction
        # text = eval(("lines_text" + str(quadrant)))
        # clean_text = [line for line in text if text[line].isalnum() == True]


        # use list slicers to clean this up 1:-1 should get front and back, check for "infraspecfic"
        if len(eval(("lines_text" + str(quadrant)))) == 2:
            family = eval(("lines_text" + str(quadrant)))[0]
            genera = eval(("lines_text" + str(quadrant)))[1].split(" ")[0]
            species = eval(("lines_text" + str(quadrant)))[1]
            common = "(None)"
        if len(eval(("lines_text" + str(quadrant)))) == 3: 
            family = eval(("lines_text" + str(quadrant)))[0]
            genera = eval(("lines_text" + str(quadrant)))[1].split(" ")[0]
            species = eval(("lines_text" + str(quadrant)))[1]
            common = eval(("lines_text" + str(quadrant)))[2]
        elif len(eval(("lines_text" + str(quadrant)))) == 4:
            if "infraspecific taxa and species status" in eval(("lines_text" + str(quadrant)))[3]:
                family = eval(("lines_text" + str(quadrant)))[0]
                genera = eval(("lines_text" + str(quadrant)))[1].split(" ")[0]
                species = eval(("lines_text" + str(quadrant)))[1]
                common = eval(("lines_text" + str(quadrant)))[2]
            else:    
                family = eval(("lines_text" + str(quadrant)))[0]
                genera = eval(("lines_text" + str(quadrant)))[1].split(" ")[0]
                species = eval(("lines_text" + str(quadrant)))[1]+ " " + eval(("lines_text" + str(quadrant)))[2]
                common = eval(("lines_text" + str(quadrant)))[3]
        elif len(eval(("lines_text" + str(quadrant)))) == 5:
            if "infraspecific taxa and species status" in eval(("lines_text" + str(quadrant)))[3]:
                family = eval(("lines_text" + str(quadrant)))[0]
                genera = eval(("lines_text" + str(quadrant)))[1].split(" ")[0]
                species = eval(("lines_text" + str(quadrant)))[1]+ " " + eval(("lines_text" + str(quadrant)))[2]
                common = eval(("lines_text" + str(quadrant)))[3]    
            else:
                family = eval(("lines_text" + str(quadrant)))[0]
                genera = eval(("lines_text" + str(quadrant)))[1].split(" ")[0]
                species = eval(("lines_text" + str(quadrant)))[1]+ " " + eval(("lines_text" + str(quadrant)))[2] + " " + eval(("lines_text" + str(quadrant)))[3]
                common = eval(("lines_text" + str(quadrant)))[4]

        cur.execute("SELECT family_id FROM family WHERE family = %s", (family,))
        family_id_test = cur.fetchone()
        cur.execute("SELECT genera_id FROM genera WHERE genera = %s", (genera,))
        genera_id_test = cur.fetchone()
        cur.execute("SELECT species_id FROM species WHERE scientific_name = %s", (species,))
        species_id_test = cur.fetchone()

        # Avoid duplicate insertions into database
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
    return
                
def main():
    print("before database")
    conn = psy.connect('dbname=postgres user=postgres password=password host=0.0.0.0 port=30420')
    print("after con before auto commit")
    conn.autocommit = True
    print("database connected")

    cur = conn.cursor()
    cur.execute("SET search_path TO ar_plants;")

    # gather county data
# TODO refactor as looping over images in the directory using os    
    phylas = {'images/gymnosperms_', 'images/pteridophytes_', 'images/angiosperm_monocots_', 'images/angiosperm_dicots_'}
    for phyla in phylas:
        for i in range(320):
            if exists(phyla + str(i) + '.jpeg') is True:
                path = phyla + str(i) + '.jpeg'
                phyla_name = str(phyla.removeprefix("images/").removesuffix("_")).replace("_", " ")
                print(path)
                process_images(cur, path, phyla_name)
                # upload_to_database(data) "maybe I wont build this function"
                continue
            else:
                continue


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