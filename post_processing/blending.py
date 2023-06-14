# Importing Required Module
from PIL import Image
# Creating a image1 object
import os
path1="/home/ceinfo/Desktop/november/output/"
path2="/home/ceinfo/Desktop/november/512/"
path3="/home/ceinfo/Desktop/november/final/"

for i in os.listdir(path1):

    image1 = Image.open(path1+i)
    # Creating a image2 object
    image2 = Image.open(path2+i)
    # As Alpha value is 0.0, Image1 would be returned
    #image3 = Image.blend(image1,image2,0.0)
    #image3.save(path3+i)
    # image3.show()

    # As Alpha value is 0.5, Blend of both would be returned
    image4 = Image.blend(image1,image2,0.7)
    image4.save(path3+i)
    # image4.show()
    # As Alpha value is 1.0, Image2 would be returned
    # image5 = Image.blend(image1,image2,1.0)
    # image5.save("output3.jpg")
    # image5.show()

