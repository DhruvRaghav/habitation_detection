import cv2
import numpy as np
import matplotlib as plt
import os

path1="/mnt/vol2/Dhruv_Raghav/general_unet_model/snapshots/test_1/"
path2="/home/ceinfo/Desktop/november/output/"
for i in os.listdir(path1):

    img = cv2.imread(path1+i, 0)
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    cv2.imwrite(path2+i,img_color)

    # plt.imwrite('/mnt/vol2/Dhruv_Rcolourisedimage.png',img_color)
    # cv2.imshow('colorized image', img_color)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()