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
text_crop_species = (241, 555, 740, 690)
text_crop_bools = (610, 420, 700, 550)
x_transform_tuple = (x_transform, 0, x_transform, 0)
y_middle_transform_tuple = (0, y_middle_transform, 0, y_middle_transform)
y_bottom_transform_tuple = (0, y_bottom_transform, 0, y_bottom_transform)

def process_images(cur, path, phyla):
    
    # y is before x when indexing into the image
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
    for quadrant in range(6):
        image = imread(path, as_gray = True)
        img = PIL.Image.open(path)
        
        # extract text data based on quadrant
        if quadrant == 0:
            quadrant0 = img.crop(text_crop_species)
            quadrant0_bool = img.crop(text_crop_bools)
            q0 = np.asarray(quadrant0)
            q_bool0 = np.asarray(quadrant0_bool)
            raw_text0 = pytesseract.image_to_string(q0)
            lines_text0 = raw_text0.splitlines()       
        elif quadrant == 1:
            quadrant1 = img.crop(tuple(np.add(text_crop_species, x_transform_tuple)))
            quadrant1_bool = img.crop(tuple(np.add(text_crop_bools, x_transform_tuple)))
            q_bool1 = np.asarray(quadrant1_bool)
            q1 = np.asarray(quadrant1)
            raw_text1 = pytesseract.image_to_string(q1)
            lines_text1 = raw_text1.splitlines()
        elif quadrant == 2:
            quadrant2 = img.crop(tuple(np.add(text_crop_species, y_middle_transform_tuple)))
            quadrant2_bool = img.crop(tuple(np.add(text_crop_bools, y_middle_transform_tuple)))
            q_bool2 = np.asarray(quadrant2_bool)
            q2 = np.asarray(quadrant2)
            raw_text2 = pytesseract.image_to_string(q2)
            lines_text2 = raw_text2.splitlines()
        elif quadrant == 3:
            quadrant3 = img.crop(tuple(np.add((tuple(np.add(text_crop_species, y_middle_transform_tuple))), x_transform_tuple)))
            quadrant3_bool = img.crop(tuple(np.add((tuple(np.add(text_crop_bools, y_middle_transform_tuple))), x_transform_tuple)))
            q3 = np.asarray(quadrant3)
            q_bool3 = np.asarray(quadrant3_bool)
            raw_text3 = pytesseract.image_to_string(q3)
            lines_text3 = raw_text3.splitlines()   
        elif quadrant == 4:
            quadrant4 = img.crop(tuple(np.add(text_crop_species, y_bottom_transform_tuple)))
            quadrant4_bool = img.crop(tuple(np.add(text_crop_bools, y_bottom_transform_tuple)))
            q4 = np.asarray(quadrant4)
            q_bool4 = np.asarray(quadrant4_bool)
            raw_text4 = pytesseract.image_to_string(q4)
            lines_text4 = raw_text4.splitlines()
        elif quadrant == 5:
            quadrant5 = img.crop(tuple(np.add((tuple(np.add(text_crop_species, y_bottom_transform_tuple))), x_transform_tuple)))
            quadrant5_bool = img.crop(tuple(np.add((tuple(np.add(text_crop_bools, y_bottom_transform_tuple))), x_transform_tuple)))
            q5 = np.asarray(quadrant5)
            q_bool5 = np.asarray(quadrant5_bool)
            raw_text5 = pytesseract.image_to_string(q5)
            lines_text5 = raw_text5.splitlines()
        else:
            return 1
        
        if eval(("lines_text" + str(quadrant)))[0].isalnum() == False:
            continue
        phyla = str(phyla.removeprefix("images/").removesuffix("_"))
        print(phyla)
        cur.execute("SELECT phyla_id FROM phyla WHERE polyphylactic_group = %s", (phyla,))
        phyla_id = cur.fetchone()[0]
        print(phyla_id)
        family = eval(("lines_text" + str(quadrant)))[0]
        genera = eval(("lines_text" + str(quadrant)))[1].split(" ")[0]
        species = eval(("lines_text" + str(quadrant)))[1]+ " " + (eval(("lines_text" + str(quadrant)))[2].split("  ")[0])
        common = eval(("lines_text" + str(quadrant)))[3]

        cur.execute("SELECT family_id FROM family WHERE family = %s", (family,))
        family_id_test = cur.fetchone()[0]
        if family_id_test == False:    
            cur.execute("INSERT INTO family VALUES (DEFAULT, %s, %s)", (family, phyla_id))
        else:
            continue
        cur.execute("SELECT family_id FROM family WHERE family = %s", (family,))
        family_id = cur.fetchone()[0]
        cur.execute("INSERT INTO genera VALUES (DEFAULT, %s, %s, %s)", (genera, family_id, phyla_id))
        print(family, genera, species, common)

        # x transform conditions
        if quadrant % 2 != 0:
            transform_x = x_transform
            transform_y = 0
        else:
            transform_x = 0
            transform_y = 0
        # y transform conditions
        if quadrant == 2 or quadrant == 3:
            transform_y = y_middle_transform
        elif quadrant == 4 or quadrant == 5:
            transform_y = y_bottom_transform 
        
        for county in counties:
            county_occurance = image[county["y"] + transform_y][county["x"] + transform_x]
            if county_occurance < 0.5:
                # species_id = cur.execute("SELECT species_id FROM species WHERE scientific_name = %s;", (VARIABLE_TODO,))
                # county_id = cur.execute("SELECT county_id FROM counties WHERE county_name = %s;", (county["name"],))
                # cur.execute("INSERT INTO county_occurance VALUES (%s, %s);", (species_id, county_id,))
                continue
    return
                
def main():
    conn = psy.connect('dbname=postgres user=postgres password=password host=host.docker.internal')
    conn.autocommit = True

    cur = conn.cursor()
    cur.execute("SET search_path TO ar_plants;")

    # gather county data
    
    phylas = {'images/gymnosperms_', 'images/pteridophytes_', 'images/angiosperm_monocots_', 'images/angiosperm_dicots_'}
    for phyla in phylas:
        for i in range(5000):
            if exists(phyla + str(i) + '.jpeg') is True:
                path = phyla + str(i) + '.jpeg'
                process_images(cur, path, phyla)
                # upload_to_database(data)
                continue
            else:
                continue


    # print(genera)

    # use config="--psm 6 digits" for retrieving numbers
    # print(pytesseract.image_to_string(q0, config="--psm 6 digits"))

    # imshow(q1)
    # plt.show()

    
main()
