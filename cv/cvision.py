'''
cvision.py
'''

import cv2, numpy as np
import matplotlib.pyplot as plt
import argparse

#for command line arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = 'Path to input image')
args = vars(ap.parse_args())

#display image
image = cv2.imread(args['image'])
#cv2.imshow('Image', image)
#cv2.waitKey(0)

#convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#edge detection
edged = cv2.Canny(gray, 30, 150)

#threshold
thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)[1]

plt.contour(thresh, cmap = 'binary')
plt.show()











