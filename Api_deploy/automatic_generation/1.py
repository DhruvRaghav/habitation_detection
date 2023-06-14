import os
import time
import cv2
import numpy as np
from PIL import Image

from data import testGenerator, saveResult
from model import unet

# folder to check for new images and tab files
src_folder = "/home/ceinfo/Desktop/2023/"
# folder to save the gray scale images
dst_folder = "/home/ceinfo/Desktop/2023_result/"
# list to store the names of the processed images
processed_images = []
# list to store the names of the files in the source folder
existing_files = []

# function to convert image to gray scale and resize it
def image_to_grey_sort_resize(input_path, dest_path):
    try:
        img = cv2.imread(input_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized_img = cv2.resize(gray, (512, 512))
        cv2.imwrite(dest_path, resized_img)
    except Exception as e:
        print("Error converting image to gray scale and resizing:", e)

while True:
    try:
        # get the list of files in the source folder
        files = os.listdir(src_folder)

        # loop through the new files that have been added
        for file in set(files) - set(existing_files):
            # get the file path
            file_path = os.path.join(src_folder, file)

            # check if the file is an image and not already processed
            if (file.endswith(".jpg") or file.endswith(".png")) and file not in processed_images:
                # get the corresponding tab file
                tab_file = file.replace(".jpg", ".tab").replace(".png", ".tab")
                tab_file_path = os.path.join(src_folder, tab_file)

                # check if the tab file exists
                if os.path.exists(tab_file_path):
                    # convert the image to gray scale and resize it
                    count = 0
                    for i in os.listdir(src_folder):
                        input_path = os.path.join(src_folder, i)
                        dest_path = os.path.join(dst_folder, str(count) + ".png")
                        image_to_grey_sort_resize(input_path, dest_path)
                        count += 1

                    num_images = count
                    print("count", count)

                    # testing the model on the converted images
                    testGene = testGenerator(dst_folder,
                                             num_image=num_images, target_size=(512, 512))
                    model = unet()
                    model.load_weights("/mnt/vol2/Dhruv_Raghav/General_unet_model/weights/hatitat_final.hdf5")
                    results = model.predict_generator(testGene, num_images, verbose=1)

                    # saving the prediction results
                    saveResult(dst_folder + "/masks/", results)

                    # gray_image_path = os.path.join(dst_folder, file)
                    # convert_to_gray(file_path, gray_image_path)

                    # add the image to the list of processed images
                    processed_images.append(file)
                else:
                    print("Tab file not found for image:", file)

        # update the list of existing files
        existing_files = files
    except Exception as e:
        print("Error reading the source folder:", e)

    # wait for 1 second before checking for new files again
    time.sleep(1)
