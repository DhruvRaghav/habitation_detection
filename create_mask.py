'''import rioxarray
import json


# load in the geojson file
with open("/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/geojson/23_Green.geojson") as igj:
    data = json.load(igj)
# if GDAL 3+
crs = data["crs"]["properties"]["name"]
# crs = "EPSG:4326" # if GDAL 2
geoms = [feat["geometry"] for feat in data["features"]]

# create empty mask raster based on the input raster
rds = rioxarray.open_rasterio("/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/tiff_images/23_data.tif").isel(band=0)
rds.values[:] = 1
rds.rio.write_nodata(0, inplace=True)

# clip the raster to the mask
clipped = rds.rio.clip(geoms, crs, drop=False)
clipped = rds.rio.clip(geoms, crs, drop=False, invert=True)
clipped.rio.to_raster("mask.tif", dtype="uint8")
'''



# import fiona
# import rasterio
# import rasterio.mask
# import gdal
#
# with fiona.open("/mnt/vol1/Sakshi_2/Forest Segmentation/mmi_data/Green_layer/2005_Green.geojson", "r") as geojson:
#    features = [feature["geometry"] for feature in geojson]
#
# with rasterio.open("/mnt/vol1/Sakshi_2/Forest Segmentation/mmi_data/tif/2005_data.tif") as src:
#    out_image, out_transform = rasterio.mask.mask(src, features, crop=True)
#    out_meta = src.meta

#environment-test_raster
#import rioxarray
import json
import matplotlib as plt
import os
path1='/home/ceinfo/Downloads/test_json'
path2='/home/ceinfo/Downloads/test_tif'
masks_path='/home/ceinfo/Downloads/test'
for file1 in os.listdir(path1):
    print(file1)
    # load in the geojson file
    with open(os.path.join(path1,file1)) as igj:
        data = json.load(igj)
    # if GDAL 3+
    crs = data["crs"]["properties"]["name"]
    # crs = "EPSG:4326" # if GDAL 2
    geoms = [feat["geometry"] for feat in data["features"]]

    # create empty mask raster based on the input raster
    rds = rioxarray.open_rasterio(os.path.join(path2,file1.split('_')[0]+"_data.tif")).isel(band=0)
    rds.values[:] = 1
    rds.rio.write_nodata(0, inplace=True)

    # clip the raster to the mask
    clipped = rds.rio.clip(geoms, crs, drop=False)
    clipped.rio.to_raster(os.path.join(masks_path,file1.split('_')[0]+"_mask.png"), dtype="uint8", interleave='Pixel')
    # input_img = plt.imread('mask.tif')
    # plt.imshow('input_img')

