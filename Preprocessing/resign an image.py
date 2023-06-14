import cv2

import os


path1="/home/ceinfo/Desktop/november/images/"
path2="/home/ceinfo/Desktop/november/512/"
for i in os.listdir(path1):

    print(i)

    img = cv2.imread(path1 +i)
    #print(img)
    resized_img = cv2.resize(img, (512, 512))
    cv2.imwrite(path2+i, resized_img)