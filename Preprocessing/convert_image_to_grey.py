import cv2
import numpy as np
import os

# reading the image
path="/mnt/vol2/Dhruv_Raghav/general_unet_model/Preprocessing/Images_after_preprocessing/sorted_mask_image/"
path2="/mnt/vol2/Dhruv_Raghav/general_unet_model/Preprocessing/train_mask/"
for i in os.listdir(path):
    img = cv2.imread(path+i)

    # converting to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # writing the grayscale image
    cv2.imwrite(path2+i, gray)