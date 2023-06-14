import numpy as np

from model import unet
from data import testGenerator, saveResult
import cv2

num_images = 217
batch_size = 2
target_size = (512, 512)

# Create a generator to load test images in batches
test_gen = testGenerator("/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/train/image/",
                          num_image=num_images,
                          target_size=target_size
                          )

# Wrap the generator with a threadsafe iterator
def threadsafe_iter(iterable):
    # this function returns an iterator which guarantees thread safety
    import threading
    lock = threading.Lock()
    iterable = iter(iterable)
    while True:
        with lock:
            try:
                yield next(iterable)
            except StopIteration:
                break
test_gen = threadsafe_iter(test_gen)

# Load the model
model = unet()
model.load_weights("/mnt/vol2/Dhruv_Raghav/general_unet_model/weights/hatitat_final.hdf5")


# Predict on test images in batches
results = []
for i in range(num_images//batch_size):
    batch = next(test_gen)
    batch_results = model.predict_on_batch(batch)
    results.append(batch_results)

# Concatenate the results
results = np.concatenate(results, axis=0)

# Save the results
saveResult("/home/ceinfo/Desktop/sat_test_data_mask/masks/", results)
