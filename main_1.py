from model import *
from data import *
import os
from model import *
from data import *

#os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Load the model
model = unet()
model.load_weights('/mnt/vol2/Dhruv_Raghav/general_unet_model/weights/hatitat_final.hdf5')

# Define data generator
data_gen_args = dict()
testGene = testGenerator("/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/train/image/",1, target_size=(256,256))

# Perform inference on folder
results = model.predict_generator(testGene,len(os.listdir("/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/train/image/")),verbose=1)
saveResult("/home/ceinfo/Desktop/sat_test_data_mask/masks/", results)
