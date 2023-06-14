from model import *
from data import *

data_gen_args = dict(rotation_range=0.2,
                    width_shift_range=0.05,
                    height_shift_range=0.05,
                    shear_range=0.05,
                    zoom_range=0.05,
                    horizontal_flip=True,
                    fill_mode='nearest')
myGene = trainGenerator(4,'/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/train','image','label',data_gen_args,save_to_dir = None,target_size=(512,512))
model = unet()
model_checkpoint = ModelCheckpoint('/mnt/vol2/Dhruv_Raghav/general_unet_model/weights/hatitat_v6.hdf5', monitor='loss',verbose=1, save_weights_only=True)
model.fit_generator(myGene,steps_per_epoch=500,epochs=20,callbacks=[model_checkpoint])

