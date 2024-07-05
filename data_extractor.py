import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imshow
import psycopg2 as psy
import pytesseract
import PIL
from os.path import exists



def process_images():
    phylas = {'images/gymnosperms_', 'images/pteridophytes_', 'images/angiosperm_monocots_', 'images/angiosperm_dicots_'}
    for phyla in phylas:
        for i in range(5000):
            while exists(phyla + str(i) + '.jpeg') is True:
                path = phyla + str(i) + '.jpeg'
                current_image = imread(path, as_gray = True)

                break
def main():
    conn = psy.connect('dbname=postgres user=postgres password=password host=host.docker.internal')
    conn.autocommit = True

    cur = conn.cursor()
    cur.execute("SET search_path TO ar_plants;")

    plt.switch_backend('TkAgg')
    
    process_images()

    image = imread('images/gymnosperms_1.jpeg', as_gray = True)
    # pixel amounts to transfer between state maps
    x_transform = 780
    y_middle_transform = 675
    y_bottom_transform = 1346

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
                species_id = cur.execute("SELECT species_id FROM species WHERE scientific_name = %s;", (VARIABLE_TODO,))
                county_id = cur.execute("SELECT county_id FROM counties WHERE county_name = %s;", (county["name"],))
                cur.execute("INSERT INTO county_occurance VALUES (%s, %s);", (species_id, county_id,))
                cur.close()
        


    text_crop_species = (241, 555, 740, 690)
    text_crop_bools = (610, 420, 700, 550)
    x_transform_tuple = (x_transform, 0, x_transform, 0)
    y_middle_transform_tuple = (0, y_middle_transform, 0, y_middle_transform)
    y_bottom_transform_tuple = (0, y_bottom_transform, 0, y_bottom_transform)

    img = PIL.Image.open("images/gymnosperms_2.jpeg")

    # crop image to isolate family, genera, and species text
    quadrant0 = img.crop(text_crop_species)
    quadrant1 = img.crop(tuple(np.add(text_crop_species, x_transform_tuple)))
    quadrant2 = img.crop(tuple(np.add(text_crop_species, y_middle_transform_tuple)))
    quadrant3 = img.crop(tuple(np.add((tuple(np.add(text_crop_species, y_middle_transform_tuple))), x_transform_tuple)))
    quadrant4 = img.crop(tuple(np.add(text_crop_species, y_bottom_transform_tuple)))
    quadrant5 = img.crop(tuple(np.add((tuple(np.add(text_crop_species, y_bottom_transform_tuple))), x_transform_tuple)))

    # turn images into NDarray's
    q0 = np.asarray(quadrant0)
    q1 = np.asarray(quadrant1)
    q2 = np.asarray(quadrant2)
    q3 = np.asarray(quadrant3)
    q4 = np.asarray(quadrant4)
    q5 = np.asarray(quadrant5)

    raw_text0 = pytesseract.image_to_string(q0)

    lines_text0 = raw_text0.splitlines()
    family = lines_text0[0]
    genera = (lines_text0[1].split(" ")[0])
    species = lines_text0[1]
    common = lines_text0[3]




    # print(genera)

    # use config="--psm 6 digits" for retrieving numbers
    # print(pytesseract.image_to_string(q0, config="--psm 6 digits"))

    # imshow(q1)
    # plt.show()




    counties1 = {
        "arkansas": image[381][556],
        "ashley":  image[526][516],
        "baxter": image[122][454],
        "benton":image[122][256],
        "boone": image[128][377],
        "bradley": image[490][473],
        "calhoun": image[480][438],
        "carroll": image[122][331],
        "chicot": image[514][565],
        "clark": image[418][368],
        "clay": image[113][651],
        "cleburne": image[225][484],
        "cleveland": image[436][474],
        "columbia": image[525][362],
        "conway": image[261][418],
        "craighead": image[186][633],
        "crawford": image[219][254],
        "crittenden": image[255][664],
        "cross": image[255][620],
        "dallas": image[428][421],
        "desha": image[447][566],
        "drew": image[475][521],
        "faulkner": image[278][455],
        "franklin": image[225][296],
        "fulton": image[116][505],
        "garland": image[351][368],
        "grant": image[388][443],
        "greene": image[150][636],
        "hempstead": image[456][316],
        "hotspring": image[386][399],
        "howard": image[414][285],
        "independence": image[202][532],
        "izard": image[155][499],
        "jackson": image[219][574],
        "jefferson": image[383][494],
        "johnson": image[222][335],
        "lafayette": image[525][321],
        "lawrence": image[163][583],
        "lee": image[322][619],
        "lincoln": image[430][519],
        "littleriver": image[462][249],
        "logan": image[263][312],
        "lonoke": image[325][504],
        "madison": image[170][310],
        "marion": image[134][415],
        "miller": image[509][290],
        "mississippi": image[189][686],
        "monroe": image[333][574],
        "montgomery": image[355][316],
        "nevada": image[468][354],
        "newton": image[128][377],
        "ouachita": image[475][393],
        "perry": image[300][395],
        "phillips": image[358][616],
        "pike": image[402][316],
        "poinsett": image[219][626],
        "polk": image[358][258],
        "pope": image[241][379],
        "prairie": image[316][538],
        "pulaski": image[325][460],
        "randolph": image[120][591],
        "saintfrancis": image[288][619],
        "saline": image[341][418],
        "scott": image[313][276],
        "searcy": image[178][416],
        "sebastian": image[265][251],
        "sevier": image[420][251],
        "sharp": image[152][538],
        "stone": image[185][465],
        "union": image[531][426],
        "vanburen": image[219][438],
        "washington": image[170][260],
        "white": image[264][516],
        "woodruff": image[269][572],
        "yell": image[294][338]
        }
    
main()
