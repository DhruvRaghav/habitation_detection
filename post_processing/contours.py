# Write a python script to generate bounding box using image mask
import os
import cv2
import numpy as np
from PIL import Image


# Read the image

path_mask="/home/ceinfo/Desktop/november/output/"
path_image="/home/ceinfo/Desktop/november/512/"
output="/mnt/vol2/Dhruv_Raghav/general_unet_model/post_processing/output/"
for i in os.listdir(path_mask):
    img_mask = cv2.imread(path_mask+i)
    # Convert the image to grayscale
    # Convert the image to grayscale
    gray = cv2.cvtColor(img_mask, cv2.COLOR_BGR2GRAY)

    # gray = cv2.cvtColor(img_mask, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to the image
    ret, thresh = cv2.threshold(gray, 127, 255, 0)

    # Find contours in the image
    _,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contourscv.drawContours(img, contours, -1, (0,255,0), 3)
    for c in contours:
        # Get the bounding rectangle of the contour
        # x, y, w, h = cv2.boundingRect(c)

        # Draw a bounding rectangle around the contour
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        img_image=cv2.imread(path_image+i)
        cv2.drawContours(img_image, contours, -2, (0, 255, 0), 2)
        cv2.imwrite(output + i,img_image)
    # Show the image
    #cv2.imshow('Image with bounding rectangle', img_image)

    # Wait for a keypress
    #cv2.waitKey(0)

    # Destroy all the windows
    #cv2.destroyAllWindows()