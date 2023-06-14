import os

import cv2
import numpy as np
path='/home/ceinfo/Downloads/Testing_data_256'



def save_as_png_count(path1,path2):
    i = 0
    for img in os.listdir(path1):
        im = cv2.imread(os.path.join(path1, img))
        # w, h, c = im.shape
        # # if (w == 256 and h == 256):
        # gray1 = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            # ret, gray1 = cv2.threshold(gray1, 127, 255, 0)
        cv2.imwrite(path2 +'/'+ str(i) + '.png', im)
        i = i + 1


def conver_bw():
    cap = cv2.imread('out.png')
    #You're free to do a resize or not, just for the example
    cap = cv2.resize(cap, (340,480))
    for x in range (0,340,1):
        for y in range(0,480,1):
            color = cap[y,x]
            print(color)

def resize_imgs():
    in_path='/mnt/vol1/Sakshi_2/Testing Data (another copy)'
    out_path='/mnt/vol1/Sakshi_2/Testing Data (another copy)'
    i = 0
    os.makedirs(out_path,exist_ok=True)
    img_list = os.listdir(in_path)
    img_list.sort()
    for img in img_list:
        im = cv2.imread(os.path.join(in_path, img))
        gray1 = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        print(img, im.shape)

        # im = cv2.resize(gray1, (512,512),interpolation=cv2.INTER_AREA)
        im=cv2.resize(gray1, (1595,795),interpolation=cv2.INTER_AREA)
        cv2.imwrite(out_path+'/' + img.split('.')[0] + '.png', im)
        i = i + 1


def resize_imgs_back():
    in_path = '/home/ceinfo/Downloads/test_2'
    out_path = '/home/ceinfo/Downloads/test_3'
    i = 0
    img_list=os.listdir(in_path)
    img_list.sort()
    for img in img_list:
        print(img)
        im = cv2.imread(os.path.join(in_path, img))
        im = cv2.resize(im, (1595,738), interpolation=cv2.INTER_AREA)

        cv2.imwrite(out_path + '/' + str(i) + '.png', im)
        i = i + 1


def print_size():
    in_path = '/home/ceinfo/Downloads/test_2'
    # out_path = '/mnt/vol1/Sakshi_2/test_unet_1'
    i = 0
    for img in os.listdir(in_path):
        print(img)
        im = cv2.imread(os.path.join(in_path, img))
        print(im.shape)


def filter_prediction(path1,path2):
    i = 0
    for img in os.listdir(path1):
        im = cv2.imread(os.path.join(path1, img))
        # w, h, c = im.shape
        # # if (w == 256 and h == 256):
        gray1 = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, gray1 = cv2.threshold(gray1, 127, 255, 0)
        cv2.imwrite(path2 +'/'+ str(i) + '.png', im)
        i = i + 1



#
# resize_imgs()
# resize_imgs_back()

# print_size()
# save_as_png_count('/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/new_masks','/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/train_data/masks')

resize_imgs()

