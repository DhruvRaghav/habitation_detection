import numpy as np
import gdal, osr
from PIL import Image
import json

# Open the satellite image and the footprint mask
img = Image.open('/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/3_data.jpg')
mask = Image.open('/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads02/masks/0_predict.png')

# Create a numpy array from the image and mask
img_arr = np.array(img)
mask_arr = np.array(mask)

# Set the no data value for the TIFF image
nodata = 0

# Create a TIFF file
driver = gdal.GetDriverByName('GTiff')
ds = driver.Create('output.tif', img.size[0], img.size[1], 1, gdal.GDT_Byte, options=['NODATA=%d' % nodata])
ds.GetRasterBand(1).WriteArray(np.where(mask_arr != 0, img_arr, nodata))

# Set the geotransform and projection
x_min = -180
y_max = 90
x_res = 360 / img.size[0]
y_res = -180 / img.size[1]
geotransform = (x_min, x_res, 0, y_max, 0, y_res)
ds.SetGeoTransform(geotransform)
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)  # WGS 84
ds.SetProjection(srs.ExportToWkt())

# Close the TIFF file
ds = None

# Open the TIFF file and convert it to a GeoJSON file
ds = gdal.Open('output.tif')
options = ['ALL_TOUCHED=FALSE', 'COMPRESS=DEFLATE']
gdal.VectorTranslate('output.geojson', ds, options=options)
