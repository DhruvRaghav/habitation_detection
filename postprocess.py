import cv2
import numpy as np
import os
# img_1 = cv2.imread('/mnt/vol1/Sakshi_2/Testing Data/1_data/0.png')
#
# img_2 = cv2.imread('/mnt/vol1/Sakshi_2/Testing Data/1_data/1.png')
# #
# # h1, w1 = img_1.shape[:2]
# # h2, w2 = img_2.shape[:2]
#
#
# img_3 = np.zeros((256, 512,3), dtype=np.uint8)
# # img_3[:,:] = (255,255,255)
#
# img_3[:256, :256,:3] = img_1
# img_3[:256, 256:,:3] = img_2
#
# cv2.imshow('Img_1',img_1)
# cv2.imshow('Img_2',img_2)
# cv2.imshow('Img_3',img_3)
# cv2.waitKey(0)


def combine(num_h,num_w,path):
    Com_image = np.zeros((256*num_h,256*num_w, 3), dtype=np.uint8)
    Com_image_mask = np.zeros((256*num_h,256*num_w,3), dtype=np.uint8)

    count=0
    for i in range(1,num_h+1):
        for j in range(1, num_w+1):
            img=cv2.imread(os.path.join(path,str(count)+".png"))
            img_mask = cv2.imread(os.path.join(path, str(count) + "_predict.png"))
            Com_image[((i-1)*256):(i*256),((j-1)*256):(j*256),:3]=img
            Com_image_mask[((i - 1) * 256):(i * 256), ((j - 1) * 256):(j * 256),:3] = img_mask
            count=count+1

    cv2.imwrite(path+'/a_grey.png',Com_image)
    cv2.imwrite(path+'/a_predict.png',Com_image_mask)



combine(3,6,'/mnt/vol1/Sakshi_2/Testing Data/0_data')