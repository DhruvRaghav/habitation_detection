import os
import cv2
def count():
    in_path="/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/habitat_train/image/"
    out_path="/home/ceinfo/Desktop/november/"
    count = 0
    img_list = os.listdir(in_path)
    img_list.sort()
    for image in img_list:
        print(image)
        img = cv2.imread(os.path.join(in_path, image))
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cropped_image = img[h1:h2,w1:w2]

        cv2.imwrite(out_path +'/'+ str(count) + ".png",img)
        count=count+1

count()