import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from skimage.io import imread, imshow
import skimage as ski

plt.switch_backend('TkAgg')

grey_image = imread('gymnosperms_1.jpeg', as_gray = True)

#coordinates are [y][x]
baxter = grey_image[122][454]
boone = grey_image[128][377]

print("Min value:", np.min(grey_image))
print("Max value:", np.max(grey_image))
print("Data type:", grey_image.dtype)

print(baxter)
print(boone)

print(grey_image[377][128])

print(grey_image.shape)
imshow(grey_image, cmap='gray')
plt.show()
