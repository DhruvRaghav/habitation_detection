
import numpy as np
import cv2
import os
from PIL import Image


path="/mnt/vol2/Dhruv_Raghav/general_unet_model/final_mask/"
path2="/mnt/vol2/Dhruv_Raghav/general_unet_model/Preprocessing/Images_after_preprocessing/images/"
for i in os.listdir(path):
    #im = Image.open(path+i)

    im = cv2.imread(path+i)

    # invert color
    img = cv2.bitwise_not(im)

    # save inverted image
    cv2.imwrite(path2+i, img)