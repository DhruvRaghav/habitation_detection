import base64
import json
import pickle

import requests
from gdal_convert import *

import cv2
from flask import Flask, request,Response
app = Flask(__name__)
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
import datetime
from model import *
from data import *
from flask import Flask, request,Response
app = Flask(__name__)
from keras import backend as K



if not (os.path.exists('Logs')):
    os.makedirs('Logs/',exist_ok=False)
log_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
handler = TimedRotatingFileHandler('Logs/'+log_filename, when='MIDNIGHT', backupCount=7)

formatter = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

# logger = logging.getLogger('werkzeug')
logger = logging.getLogger('gunicorn.error')

handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.setLevel(logger.level)
logger.addHandler(handler)

logger.propagate = False







def image_to_grey_sort_resize(input_path,dest_path2):
    import cv2
    import numpy as np
    import os
    input_path =input_path
    dest_path2 = dest_path2
    # reading the image
    count=0
    for i in os.listdir(input_path):
        img = cv2.imread(input_path + i)

        # converting to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized_img = cv2.resize(gray, (512, 512))

        # writing the grayscale image
        cv2.imwrite(dest_path2 +'/'+ str(count) + ".png",resized_img)
        count=count+1

    return count




def func3(image,bounds,scale):

    '''  TO RETURN PIXELS  IT REQUIRES : IMAGE IN jpg FORM  & GEOTAG : 2 '''







    '''--------------------------------------------------------------------'''

    '''TO CREATE THE INPUT IMAGE FOLDER'''
    path = os.getcwd()
    '''Directory'''
    directory = "uploads01"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path1 = os.path.join(parent_dir, directory)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path1, exist_ok=True)
    except OSError as error:
        pass
    '''--------------------------------------------------------------------'''

    image.save(path1+"/"+"3_data.jpg")





    '''--------------------------------------------------------------------'''

    ''' TO CREATE MASK FOLDER AND GREY SCALE IMAGE'''
    path = os.getcwd()
    '''Directory'''
    directory = "uploads02"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path2 = os.path.join(parent_dir, directory)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path2, exist_ok=True)
    except OSError as error:
        pass
    '''--------------------------------------------------------------------'''









    '''-----------------------------------------------------------------'''
    '''PREPROCESSING TESTING IMAGE'''
    input_path = path1+"/"
    output_path = path2+"/"

    count = image_to_grey_sort_resize(input_path, output_path)
    num_images = count
    #print("count", count)

    '''-----------------------------------------------------------------'''
    testGene = testGenerator(output_path,num_image=num_images,
                              target_size=(512, 512))

    model = unet()
    model.load_weights("../weights/hatitat_final.hdf5")
    results = model.predict_generator(testGene, num_images, verbose=1)


    '''-----------------------------------------------------------------'''
    path = output_path
    '''Directory'''
    directory = "masks"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path3 = os.path.join(parent_dir, directory)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path3, exist_ok=True)
    except OSError as error:
        pass
    '''--------------------------------------------------------------------------'''








    '''SAVING PREDICTION RESULTS '''
    saveResult(path3+"/", results)
    K.clear_session()
    image = cv2.imread(input_path+"3_data.jpg")
    h, w, c = image.shape


    y = 0
    x = 0
    h = h
    w = w
    crop_image = image[x:w, y:h]
    cv2.imwrite(input_path+"3_data.jpg", crop_image)

    '''----------------------------------------'''
    sw_lat = bounds['_southWest']['lat']
    sw_long = bounds['_southWest']['lng']
    ne_lat = bounds['_northEast']['lat']
    ne_long = bounds['_northEast']['lng']
    southwest = [str(sw_lat), str(sw_long)]
    print(southwest[0])
    print(southwest[1])

    northeast = [str(ne_lat), str(ne_long)]
    print(northeast[0])
    print(northeast[1])
    path1=input_path
    get1="3_data.jpg"

    values={}

    '''-----------------------------------------------------'''
    static_file = request.files['file']

    filename = static_file.filename

    content_type = static_file.content_type
    # bounds= pickle.dumps(bounds)
    # values["bounds"] = bounds

    # print("bounds",    values["bounds"])

    with open("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/3_data.jpg", "rb") as r2:
        converted_string_1 = base64.b64encode(r2.read())

    mask = json.dumps({'I M G': converted_string_1.decode('utf-8')})
    #print(mask)

    url = 'http://10.10.21.159:7010/satellite_tiff/'
    files = [('converted_string',converted_string_1), ('ulx',  southwest[0]),('uly',southwest[1]),('vlx',northeast[0]),('vly',northeast[1])]

    values["ulx"] = southwest[0]
    # print(values["southwest"])
    values["uly"] = southwest[1]
    values["vlx"] = northeast[0]
    values["vly"] = northeast[1]
    values["converted_string"] = mask


    headers = {}
    r = requests.request("POST", url, files=files, data=values, headers=headers)
    r=r.content
    # return("work in progress")

    decodeit = open('/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/tiff_image/1.tif', 'wb')
    decodeit.write(base64.b64decode((r)))
    decodeit.close()


    '''-----------------------------------------------------'''
    # # passage=gdal_convert(path1,get1,southwest,northeast)
    # # print(passage)
    #
    #
    with open("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/tiff_image/1.tif", "rb") as r1:
        converted_string =  base64.b64encode(r1.read())
#     #

    img = cv2.imread(path3+"/"+"0_predict.png")
    resized_img = cv2.resize(img,(1595,785))


    cv2.imwrite(path3+"/"+"0_predict.png", resized_img)
    with open(path3+"/"+"0_predict.png", "rb") as r2:
        converted_string_1 = base64.b64encode(r2.read())

    # os.remove(passage+"/"+"3_data.tif")

    values={}

    mask = json.dumps({'T I F': converted_string.decode(('utf-8')), 'M A S K': converted_string_1.decode(('utf-8'))})


    static_file = request.files['file']

    filename = static_file.filename

    content_type = static_file.content_type

    url = 'http://10.10.21.227:7005/satellite_model/'
    files = [('file', (filename, static_file.read(), content_type)), ('mask', mask)]

    values["mask"] = mask

    headers = {}
    r = requests.request("POST", url, files=files, data=values, headers=headers)

    os.remove(path3+"/"+"0_predict.png")
    os.remove(output_path+"0.png")
    os.remove(input_path+"3_data.jpg")


    if r.status_code == 200:

        return json.loads(r.text)
    else:
        return json.loads(
            '{"error": "Something went wrong while processing image", "status_code": 500}'), 500








def func2(image,scale):
    '''  TO RETURN PIXELS  IT REQUIRES : IMAGE IN jpg FORM  & GEOTAG : 2 '''
    path = os.getcwd()
    '''Directory'''
    directory = "uploads05"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path1 = os.path.join(parent_dir, directory)
    # print("path1",path1)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path1, exist_ok=True)
    except OSError as error:
        pass

    image.save(path1+"/"+"3_data.jpg")
    '''-----------------------------------------------------------------'''
    '''PREPROCESSING TESTING IMAGE'''
    input_path = path1+"/"

    '''--------------------------------------------------------------------'''

    ''' TO CREATE MASK FOLDER AND GREY SCALE IMAGE'''
    path = os.getcwd()
    '''Directory'''
    directory = "uploads02"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path2 = os.path.join(parent_dir, directory)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path2, exist_ok=True)
    except OSError as error:
        pass
    '''--------------------------------------------------------------------'''


    output_path = path2+"/"

    count = image_to_grey_sort_resize(input_path, output_path)
    num_images = count
    #print("count", count)

    '''-----------------------------------------------------------------'''
    testGene = testGenerator(output_path,num_image=num_images,
                              target_size=(512, 512))

    model = unet()
    model.load_weights("../weights/hatitat_final.hdf5")
    results = model.predict_generator(testGene, num_images, verbose=1)
    '''-----------------------------------------------------------------'''



    '''-----------------------------------------------------------------'''
    path = output_path
    '''Directory'''
    directory = "masks"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path3 = os.path.join(parent_dir, directory)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path3, exist_ok=True)
    except OSError as error:
        pass
    '''--------------------------------------------------------------------------'''






    '''SAVING PREDICTION RESULTS '''
    saveResult(path3+"/", results)
    K.clear_session()
    image = cv2.imread(path1+"/"+"3_data.jpg")
    h, w, c = image.shape
    # print('width:  ', w)
    # print('height: ', h)
    # print('channel:', c)


    y = 0
    x = 0
    h = h
    w = w
    crop_image = image[x:w, y:h]
    cv2.imwrite(path1+"/"+"3_data.jpg", crop_image)

    '''----------------------------------------'''
    # sw_lat = bounds['_southWest']['lat']
    # # print(sw_lat)
    # sw_long = bounds['_southWest']['lng']
    # # print(sw_long)
    # ne_lat = bounds['_northEast']['lat']
    # # print(ne_lat)
    # ne_long = bounds['_northEast']['lng']
    # # print(ne_long)
    # southwest = [str(sw_lat), str(sw_long)]
    #
    # # print(southwest)
    # northeast = [str(ne_lat), str(ne_long)]
    # # print(northeast)
    # path1="/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/"
    # get1="3_data.jpg"
    # gdal_convert(path1,get1,southwest,northeast)
    # # geojson5()


    with open(path1+"/"+"3_data.jpg", "rb") as r1:
        converted_string = base64.b64encode(r1.read())
    #

    img = cv2.imread(path3+"/"+"0_predict.png")
    #print(img)
    resized_img = cv2.resize(img,(1595,785))
    cv2.imwrite(path3+"/"+"0_predict.png", resized_img)
    with open(path3+"/"+"0_predict.png", "rb") as r2:
        converted_string_1 = base64.b64encode(r2.read())


    values={}
    #os.remove("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads02/masks/0_predict.png")
    # os.remove("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/tiff_image/3_data.tif")
    # os.remove("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/3_data.jpg")
    # os.remove("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads02/0.png")

    # os.remove("/home/ceinfo/PycharmProjects/Satellite_part_2/1.jpg")


    mask = json.dumps({'T I F': converted_string.decode('utf-8'), 'M A S K': converted_string_1.decode(('utf-8'))})

    static_file = request.files['file']

    filename = static_file.filename

    content_type = static_file.content_type

    url = 'http://10.10.21.227:7005/satellite_model_2/'
    files = [('file', (filename, static_file.read(), content_type)), ('mask', mask)]
    #print("files", files)
    # values["geotag"] = request.form['geotag']
    #print("geotag", values)
    # values["scale"] = request.form['scale']
    # values["img_type"] = request.form['img_type']
    values["mask"] = mask

    headers = {}
    r = requests.request("POST", url, files=files, data=values, headers=headers)

    os.remove(path3+"/"+"0_predict.png")
    os.remove(path2+"/"+"0.png")
    os.remove(path1+"/"+"3_data.jpg")


    if r.status_code == 200:

        return json.loads(r.text)
    else:
        return json.loads(
            '{"error": "Something went wrong while processing image", "status_code": 500}'), 500











def func1(image,scale):
    '''  TO RETURN PIXELS  IT REQUIRES : IMAGE IN jpg FORM  & GEOTAG : 2 '''
    path = os.getcwd()
    '''Directory'''
    directory = "uploads04"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path1 = os.path.join(parent_dir, directory)
    # print("path1",path1)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path1, exist_ok=True)
    except OSError as error:
        pass

    image.save(path1+"/"+"3_data.jpeg")

    '''-----------------------------------------------------------------'''
    '''PREPROCESSING TESTING IMAGE'''
    input_path = path1+"/"

    '''--------------------------------------------------------------------'''

    ''' TO CREATE MASK FOLDER AND GREY SCALE IMAGE'''
    path = os.getcwd()
    '''Directory'''
    directory = "uploads02"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path2 = os.path.join(parent_dir, directory)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path2, exist_ok=True)
    except OSError as error:
        pass
    '''--------------------------------------------------------------------'''

    output_path = path2+"/"

    count = image_to_grey_sort_resize(input_path, output_path)
    num_images = count
    #print("count", count)

    '''-----------------------------------------------------------------'''
    testGene = testGenerator(output_path,num_image=num_images,
                              target_size=(512, 512))

    model = unet()
    model.load_weights("../weights/hatitat_final.hdf5")
    results = model.predict_generator(testGene, num_images, verbose=1)
    '''-----------------------------------------------------------------'''




    '''-----------------------------------------------------------------'''
    path = output_path
    '''Directory'''
    directory = "masks"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path3 = os.path.join(parent_dir, directory)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path3, exist_ok=True)
    except OSError as error:
        pass
    '''--------------------------------------------------------------------------'''


    '''SAVING PREDICTION RESULTS '''
    saveResult(path3+"/", results)
    K.clear_session()
    image = cv2.imread(path1+"/"+"3_data.jpeg")
    h, w, c = image.shape
    # print('width:  ', w)
    # print('height: ', h)
    # print('channel:', c)


    y = 0
    x = 0
    h = h
    w = w
    crop_image = image[x:w, y:h]
    cv2.imwrite(path1+"/"+"3_data.jpeg", crop_image)

    '''----------------------------------------'''


    with open(path1+"/"+"3_data.jpeg", "rb") as r1:
        converted_string = base64.b64encode(r1.read())



    img = cv2.imread(path3+"/"+"0_predict.png")
    #print(img)
    resized_img = cv2.resize(img,(1595,785))
    cv2.imwrite(path3+"/"+"0_predict.png", resized_img)
    with open(path3+"/"+"0_predict.png", "rb") as r2:
        converted_string_1 = base64.b64encode(r2.read())


    values={}
    #os.remove("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads02/masks/0_predict.png")
    # os.remove("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/tiff_image/3_data.tif")
    # os.remove("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/3_data.jpg")
    # os.remove("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads02/0.png")

    # os.remove("/home/ceinfo/PycharmProjects/Satellite_part_2/1.jpg")


    mask = json.dumps({'T I F': converted_string.decode('utf-8'), 'M A S K': converted_string_1.decode(('utf-8'))})

    static_file = request.files['file']

    filename = static_file.filename

    content_type = static_file.content_type

    url = 'http://10.10.21.227:7005/satellite_model_1/'
    files = [('file', (filename, static_file.read(), content_type)), ('mask', mask)]
    #print("files", files)
    # values["geotag"] = request.form['geotag']
    #print("geotag", values)
    # values["scale"] = request.form['scale']
    # values["img_type"] = request.form['img_type']
    values["mask"] = mask

    headers = {}
    r = requests.request("POST", url, files=files, data=values, headers=headers)

    os.remove(path1+"/"+"3_data.jpeg")
    os.remove(path3+"/"+"0_predict.png")
    os.remove(path2+"/"+"0.png")
    # os.remove("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads04/3_data.jpg")
    if r.status_code == 200:

        return json.loads(r.text)
    else:
        return json.loads(
            '{"error": "Something went wrong while processing image", "status_code": 500}'), 500









@app.route('/Hab/',methods=['POST'])
def Hab():
    print("Welcome to Habitation Detection:")
    resp=Response(status=200,content_type='application/json')
    image = request.files['file']  # Single image path
    # print("image",image)
    # image = request.files.get('file', '')
    scale = int(request.form.get('scale'))


    # try:
    try:
        if(request.content_type!=None):
             if request.content_type.startswith('multipart/form-data'):
                 # print(request.content_type.startswith('multipart/form-data'))
                 if 'file' and 'geotag'and 'scale' in request.form.keys():
                    geotag = request.form.get('geotag')
                    #get1 = image.filename
                    # print("full file name",get1)
                    get1=image.filename.split('.')[1]
                    # print("extension", get2)
                    # get3=image.filename.split('.')[0]
                    # print("filename",get3)

                    if (get1 == 'tif' and geotag == "1"):
                        # print("it is a tiff image")
                        resp = func1(image, scale)
                        return resp

                    elif ((get1 == "jpg" or "png" or "jpeg") and geotag == "0"):
                        # bounds = eval(request.form.get('bounds'))
                        # print(bounds)
                        resp = func2(image, scale)
                        return resp


                    elif (geotag=='2' and ('bounds' in request.form.keys())):
                        # print("inside function 3")
                        bounds = eval(request.form.get('bounds'))
                        resp=func3(image,bounds,scale)
                        return resp
                    else:
                                    resp.status_code = 400
                                    return resp

                 else:
                    return json.loads('{"error": "Invalid Inputs parameters", "status_code": 400}'), 400



             else:

                 resp.status_code = 400
                 return resp
        else:

            resp.status_code = 400
            return resp

    except Exception as e:
            logger.error(msg=str(e), status_code=500)
            resp.status_code = 500
            print(e)
            return resp










if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)