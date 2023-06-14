def geojson5(path1,in_file):

    # print(path1)
    # print(in_file)
    # geoimg=geoio.GeoImage('/mnt/vol1/Downloads/filename.tif')
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

    with open(path1+"/"+in_file+'.geojson','w') as fp:
           json.dump(d, fp) # for the geojson saving uncomment #for fronend we need to comment this line
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
