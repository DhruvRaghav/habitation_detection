from model import *
from data import *
import cv2
# from preprocess import *
# from postprocess import *
image='/home/ceinfo/Downloads/test_1/21.png'
# im=cv2.imread(image)
# im=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
img = io.imread(image,as_gray = True)
target_size=img.shape
img = img / 255
img = trans.resize(img,target_size)
print(img.shape)

img = np.reshape(img,img.shape+(1,))
print(img.shape)
img = np.reshape(img,(1,)+img.shape)
print(img.shape)
print(img[0].shape[0])


# yield img
# img = np.expand_dims(img,axis=0)
# img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# img = np.expand_dims(img, axis=0)
# image_path='/mnt/vol1/Sakshi_2/Testing Data/1_data/'
# h,w,num_images=preprocess_image(image, image_path)
# num_images=16
# # # print(num_images)
# testGene = testGenerator("/home/ceinfo/Downloads/test", num_image=num_images, target_size=(1595,738))
model = unet()
model.load_weights("forest/Forest_v2_shaffled_512_v2.hdf5")
pred_mask = model.predict(img,verbose=1)
print(pred_mask)
# results = model.predict_generator(testGene,num_images,verbose=1)
# saveResult("/home/ceinfo/Downloads/test",results)
# # combine(h,w,'/mnt/vol1/Sakshi_2/Testing Data')