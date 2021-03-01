# TASK -- CREATE YOUR OWN CARTOONIZER

# IMPORT PACKAGES INCLUDING math,skimage,numpy,scipy and matplotlib

from skimage import data
from skimage.color import rgb2gray,gray2rgb
from skimage.filters import gaussian,median
from skimage import io
from skimage.feature import canny
import numpy as np
import PIL
import os
import matplotlib.pyplot as plt
import sys
from skimage.filters import median
import math

# Function Cartoonizer , is used to convert an input image to its cartoon version
def CartoonNizer_ID(image):
    # The function resturns gaussian value of the iamge
    def gaussian_own(x, sigma):
        return (1.0 / (2 * math.pi * (sigma ** 2))) * math.exp(- (x ** 2) / (2 * sigma ** 2))
    # The function finds eucledian distance between two points
    def distance(x, y, i, j):
        return np.sqrt((x-i)**2 + (y-j)**2)
    # The function applies bialteral filter formulas
    # Bilateral fucntion - caller
    def apply_bilateral_filter(source, filtered_image, x, y, diameter, sigma_i, sigma_s):
        hl = diameter/2
        i_filtered = 0
        Wp = 0
        i = 0
        while i < diameter:
            j = 0
            while j < diameter:
                neighbour_x = x - (hl - i)
                neighbour_y = y - (hl - j)
                if neighbour_x >= len(source):
                    neighbour_x -= len(source)
                if neighbour_y >= len(source[0]):
                    neighbour_y -= len(source[0])
                gi = gaussian_own(source[int(neighbour_x)][int(neighbour_y)] - source[x][y], sigma_i)
                gs = gaussian_own(distance(neighbour_x, neighbour_y, x, y), sigma_s)
                w = gi * gs
                i_filtered += source[int(neighbour_x)][int(neighbour_y)] * w
                Wp += w
                j += 1
            i += 1
        i_filtered = i_filtered / Wp
        filtered_image[x][y] = int(round(i_filtered))

    # Bilateral function - Main
    def bilateral_filter_own(source, filter_diameter, sigma_i, sigma_s):
        filtered_image = np.zeros(source.shape)

        i = 0
        while i < len(source):
            j = 0
            while j < len(source[0]):
                # Bilateral function - caller
                apply_bilateral_filter(source, filtered_image, i, j, filter_diameter, sigma_i, sigma_s)
                j += 1
            i += 1
        return filtered_image

    grayimg=rgb2gray(image)
    overlay2=gray2rgb(bilateral_filter_own(grayimg, 5, 12.0, 16.0))
    background=median(gaussian(image))
    overlay=gray2rgb(canny(rgb2gray(image)))

    alpha=0.5
    newimg=background*alpha+overlay*(1-alpha)
    newimg2=background*alpha+(overlay2)*(1-alpha)


    plt.imshow(newimg2,cmap='jet', interpolation='nearest')
    plt.show()
    io.imsave("CartoonImage.JPG",newimg2)
# Input the image
image=io.imread("img2.JPG")
CartoonNizer_ID(image)