'''************************** Hello, Lets do it ************************************************ '''

''' >>>>>>>>>>>>>>>>>>>>> Okay this is the main file.  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,  '''
from model import *
from data import *
import cv2

'''*************************************************************************'''
input_path = "/home/ceinfo/Desktop/sat_test_data/"
dest_path2 = "/home/ceinfo/Desktop/sat_test_data_mask"
'''*************************************************************************'''


def image_to_grey_sort_resize(input_path,dest_path2):
    import cv2
    import numpy as np
    import os
    input_path =input_path
    dest_path2 = dest_path2
    # reading the image
    count=0
    for i in os.listdir(input_path):
        img = cv2.imread(input_path + i)

        # converting to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized_img = cv2.resize(gray, (512, 512))

        # writing the grayscale image
        cv2.imwrite(dest_path2 +'/'+ str(count) + ".png",resized_img)
        count=count+1

    return count





if __name__ == '__main__':

    '''-----------------------------------------------------------------'''
    '''PREPROCESSING TESTING IMAGE'''

    count=image_to_grey_sort_resize(input_path,dest_path2)
    num_images = count
    print("count",count)

    '''-----------------------------------------------------------------'''
    ''' testing starts here '''

    testGene = testGenerator(dest_path2,
                             num_image=num_images, target_size=(512, 512))

    model = unet()

    model.load_weights("/mnt/vol2/Dhruv_Raghav/general_unet_model/weights/hatitat_final.hdf5")

    results = model.predict_generator(testGene, num_images, verbose=1)

    '''-----------------------------------------------------------------'''
    '''SAVING PREDICTION RESULTS '''

    saveResult(dest_path2+"/masks/", results)
    '''-----------------------------------------------------------------'''
