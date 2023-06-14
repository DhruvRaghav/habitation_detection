import cv2
image = cv2.imread("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/3_data.jpg")

y=0
x=0
h=1595
w=785
crop_image = image[x:w, y:h]
cv2.imwrite("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/cropped.jpg",crop_image)
# cv2.imshow("Cropped", crop_image)
# cv2.waitKey(0)