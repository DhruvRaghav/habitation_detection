import cv2

import os


path1="/mnt/vol2/Dhruv_Raghav/general_unet_model/post_processing/output//"
path2="/home/ceinfo/Desktop/november/resize_image/"
for i in os.listdir(path1):

    print(i)

    img = cv2.imread(path1 +i)
    #print(img)
    resized_img = cv2.resize(img,(1595,785))
    cv2.imwrite(path2+i, resized_img)