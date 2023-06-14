import geoio
import cv2
import json
import os
import subprocess
from PIL import Image
import datetime
#
# def geojson1(path1,in_file):
#     #print(path1)
#     geoimg = geoio.GeoImage(os.path.join(path1,(in_file+'.jpeg')))
#
#     #print(geoimg)
#     #print(path1)
#     #print(in_file)
#     #os.remove(os.path.join('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/',in_file+'.tif'))
#     img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
#     #print(img)
#     # os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'_mask.jpg'))
#     gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
#     ret,gray=cv2.threshold(gray,127,255,0)
#     contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#     #print(contours)
#     polygon = []
#     Features = []
#     Features1 = []
#
#     a=[]
#     for cnt in contours[1]:
#         new_filter = []
#         for j,i in enumerate(cnt):
#
#             x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
#             #print(x)
#             #print(x,y)
#             a.append(i.tolist())
#             #if(x<90.0 and x > 60.0 and y <40.0 and y>10.0):
#             new_filter.append([x, y])
#         #Features.append({"type": "features", "properties": {}, "geometry": new_filter})
#         Features.append({"type": "feature", "properties":{},"geometry":new_filter})
#         #print(Features)
#         #Features1.append({"type":"feature","properties":{},"geometry": [a]})
#         Features1.append({"type": "features", "properties": {}, "geometry": {"type": "polygon", "coordinates": a}})
#     #print(Features)
#     #print(a)
#     #print(Features1)
#
#     #print(Features1)
#     d = {"type": "FeatureCollection","features":Features}
#     print(d)
#     p = {"type": "FeatureCollection", "features":Features1}
#     #print(d)
#     #print(p)
#     c={"LAT-LONGS ":d,"PIXELS ":p}
#     #print(c)
#     #c={"PIXELS":d}
#     #os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'.TAB'))
#     with open(path1+"/"+'122222'+'.geojson','w') as fp:
#            json.dump(c, fp) # for the geojson saving uncomment #for fronend we need to comment this line
#     #return c
#     #return {" LAT-LONGS":d}
#


def geojson(tif_file,mask_file):
    #print(path1)
    geoimg = geoio.GeoImage(tif_file)
    img=cv2.imread(mask_file)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    Features_p = []
    Features_l = []
    for cnt in contours[1]:
        if (len(cnt > 2)):
            new_filter_p=[]
            new_filter_l = []
            first_p=[]
            first_l=[]
            for j,i in enumerate(cnt):
                x1=int(i[0][0])
                y1=int(i[0][1])
                x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
                # a.append(i.tolist())
                if(len(new_filter_l)==0):
                    first_l.append(x)
                    first_l.append(y)
                    first_p.append(x1)
                    first_p.append(y1)

                new_filter_p.append([x1,y1])
                new_filter_l.append([x, y])
            # new_filter_p.append(first)
            new_filter_l.append(first_l)
            new_filter_p.append(first_p)

            Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_p]}})
            Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})
    d = {"type": "FeatureCollection","features":Features_l}
    print(d)
    p = {"type": "FeatureCollection", "features":Features_p}
    c={"Locations":d,"Pixels":p}
    # with open(path1+"/"+'122222'+'.geojson','w') as fp:
    #        json.dump(c, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    return c



def geojson2(mask_file):

    #geoimg = geoio.GeoImage(os.path.join(path1,(in_file+'.jpg')))
    # print(path1)
    # print(in_file)
    img=cv2.imread(mask_file)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    # polygon = []
    Features_p = []
    # Features_l = []

    # a=[]
    for cnt in contours[1]:
        if(len(cnt>2)):

            new_filter_p=[]
            # new_filter_l = []
            # first=[]
            first_p=[]
            x2=0
            y2=0
            for j,i in enumerate(cnt):
               # print(j,i)
                x1=int(i[0][0])
                y1=int(i[0][1])
                if(len(new_filter_p)==0):
                     first_p.append(x1)
                     first_p.append(y1)
                new_filter_p.append([x1,y1])
            new_filter_p.append(first_p)


            Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_p]}})
            # Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})
    # d = {"type": "FeatureCollection","features":Features_p}
    #print(d)
    p = {"type": "FeatureCollection", "features":Features_p}
    #print(d)
    #print(p)
    c={"Pixels":p}
    #print(c)
    #c={"PIXELS":d}
    #os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'.TAB'))
    # with open(path1+"/"+'122222'+'.geojson','w') as fp:
    #        json.dump(c, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    # #return c
    # return {"Locations":d,"Pixels":p}
    return {"Pixels":p}


def geojson3(path1,in_file):


    print(path1)
    print(in_file)

    geoimg = geoio.GeoImage(os.path.join(path1+"/"+in_file+".tif"))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    Features_p = []
    Features_l = []
    for cnt in contours[1]:
        if(len(cnt>2)):

            new_filter_p=[]
            new_filter_l = []
            first_p=[]
            first_l=[]
            for j,i in enumerate(cnt):
                x1=int(i[0][0])
                y1=int(i[0][1])
                x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
                # a.append(i.tolist())
                if(len(new_filter_l)==0):
                    first_l.append(x)
                    first_l.append(y)
                    first_p.append(x1)
                    first_p.append(y1)

                new_filter_p.append([x1,y1])
                new_filter_l.append([x, y])
            # new_filter_p.append(first)
            new_filter_l.append(first_l)
            new_filter_p.append(first_p)

            Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_p]}})
            Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})
    d = {"type": "FeatureCollection","features":Features_l}
    print(d)
    p = {"type": "FeatureCollection", "features":Features_p}
    c={"Locations":d}
    with open(path1+"/"+in_file+'.geojson','w') as fp:
           json.dump(d, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    # os.remove(path1+"/"+in_file+'.jpg')
    # os.remove(path1 + "/" + in_file + '_mask.png')
    # os.remove(path1 + "/" + in_file + '.TAB')
    # os.remove(path1 + "/" + in_file + '.tif')
    # os.remove(path1 + "/" + "122222" + '.geojson')

    #ds = Image.open(path1 + "/" + in_file + '.tif')
    #print("ds",type(ds))

    return c



def geojson4(path1,in_file):
    #print(path1)
    geoimg = geoio.GeoImage(os.path.join(path1,(in_file+'.jpg')))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    Features_p = []
    Features_l = []
    for cnt in contours[1]:
        if(len(cnt>2)):

            new_filter_p=[]
            new_filter_l = []
            first_p=[]
            first_l=[]
            for j,i in enumerate(cnt):
                x1=int(i[0][0])
                y1=int(i[0][1])
                x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
                # a.append(i.tolist())
                if(len(new_filter_l)==0):
                    first_l.append(x)
                    first_l.append(y)
                    first_p.append(x1)
                    first_p.append(y1)

                new_filter_p.append([x1,y1])
                new_filter_l.append([x, y])
            # new_filter_p.append(first)
            new_filter_l.append(first_l)
            new_filter_p.append(first_p)
            Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_p]}})
            Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})

    d = {"type": "FeatureCollection","features":Features_l}
    print('dict', d)
    p = {"type": "FeatureCollection", "features":Features_p}
    c={"Locations":d}
    with open(path1+"/"+in_file+'.geojson','w') as fp:
           json.dump(d, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    return c




def geojson5(tif_file,mask_file):

    # print(path1)
    # print(in_file)
    # geoimg=geoio.GeoImage('/mnt/vol1/Downloads/filename.tif')
    # geoimg = geoio.GeoImage(os.path.join(path1+"/"+in_file+".tif"))
    geoimg=geoio.GeoImage(tif_file)
    img=cv2.imread(mask_file)
    # img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    Features_p = []
    Features_l = []
    for cnt in contours[1]:
        # print(len(cnt))
        if(len(cnt>2)):
            new_filter_p=[]
            new_filter_l = []
            first_p=[]
            first_l=[]
            for j,i in enumerate(cnt):
                x1=int(i[0][0])
                y1=int(i[0][1])
                x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
                # a.append(i.tolist())
                if(len(new_filter_l)==0):
                    first_l.append(x)
                    first_l.append(y)
                    first_p.append(x1)
                    first_p.append(y1)

                new_filter_p.append([x1,y1])
                new_filter_l.append([x, y])
            # new_filter_p.append(first)
            new_filter_l.append(first_l)
            new_filter_p.append(first_p)

            Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_p]}})
            Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})
    d = {"type": "FeatureCollection","features":Features_l}
    # print(d)
    p = {"type": "FeatureCollection", "features":Features_p}
    c={"Locations":d}

    # with open(path1+"/"+in_file+'.geojson','w') as fp:
    #        json.dump(d, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    # os.remove(path1+"/"+in_file+'.jpg')
    # os.remove(path1 + "/" + in_file + '_mask.png')
    # os.remove(path1 + "/" + in_file + '.TAB')
    # os.remove(path1 + "/" + in_file + '.tif')
    # os.remove(path1 + "/" + "122222" + '.geojson')

    #ds = Image.open(path1 + "/" + in_file + '.tif')
    #print("ds",type(ds))
    # subprocess.call('ogr2ogr -f GeoJSON /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/filename.geojson  /home/ceinfo/Desktop/new_check.geojson -t_srs EPSG:3857')
    print('geojson',datetime.datetime.now())
    # print(c)
    return c








if __name__ == '__main__':
    geojson5("/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/","sat_image_12022-09-13_19:40:10_046028.jpg")