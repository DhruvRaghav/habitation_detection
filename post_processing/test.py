
from skimage.morphology import binary_dilation, disk
from skimage.io import imread
import matplotlib.pyplot as plt

# Read in the image
image = imread("/mnt/vol2/Dhruv_Raghav/general_unet_model/post_processing/output1.jpg", as_gray=True)

# Apply a binary dilation with a disk of radius 5
dilated_image = binary_dilation(image, disk(5))

# Plot the original and the dilated image
fig, axes = plt.subplots(1, 2, figsize=(8, 4))
ax = axes.ravel()
ax[0].imshow(image, cmap="gray")
ax[0].set_title("Original image")
ax[1].imshow(dilated_image, cmap="gray")
ax[1].set_title("Dilated image")

plt.show()