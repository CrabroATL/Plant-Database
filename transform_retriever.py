import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imshow
import psycopg2 as psy
import pytesseract
import PIL
from os.path import exists

plt.switch_backend('TkAgg')

image = imread("images/gymnosperms_1.jpeg", as_gray = True)

imshow(image)
plt.show()


list = ['zero', 'one', 'two', 'three']
