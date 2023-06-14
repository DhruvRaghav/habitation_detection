import cv2
import os
# img=cv2.imread("/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/habitat_train/image/11.jpg")
# h1, w1 = img.shape[:2]
# print(h1,w1)
#
#
# def input_image(in_path,out_path,w1,w2,h1,h2):
#     # create_tiff_images(in_path,out_path)
#     count = 0
#     img_list = os.listdir(in_path)
#     img_list.sort()
#     for image in img_list:
#         print(image)
#         img = cv2.imread(os.path.join(in_path, image))
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         cropped_image = img[h1:h2,w1:w2]
#
#         cv2.imwrite(out_path +'/'+ str(count) + ".png", cropped_image)
#         count=count+1
#
#
# input_image("/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/habitat_train/image",
#              "/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/habitat_train/cropped_image",0,)





from PIL import Image

#Read image
path="/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/habitat_train/label/"
path2="/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/habitat_train/test_4/"
for i in os.listdir(path):
    im = Image.open(path+i)

    #define crop parameters
    width, height = im.size
    left = (width - 512)/2
    top = (height - 512)/2
    right = (width + 512)/2
    bottom = (height + 512)/2

    #crop image
    im = im.crop((left, top, right, bottom))

    #save cropped image
    i=i[:-4]
    print(i)
    im.save(path2+i+".png")