import base64
import json
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



input_path = "/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/"
output_path = "/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads02/"



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




def func3(image,get1,get3,bounds):
    '''  TO RETURN PIXELS  IT REQUIRES : IMAGE IN jpg FORM  & GEOTAG : 2 '''
    path = os.getcwd()
    '''Directory'''
    directory = "uploads01"
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

    count = image_to_grey_sort_resize(input_path, output_path)
    num_images = count
    #print("count", count)

    '''-----------------------------------------------------------------'''
    testGene = testGenerator(output_path,num_image=num_images,
                              target_size=(512, 512))

    model = unet()
    model.load_weights("/mnt/vol2/Dhruv_Raghav/general_unet_model/weights/hatitat_final.hdf5")
    results = model.predict_generator(testGene, num_images, verbose=1)
    '''-----------------------------------------------------------------'''
    '''SAVING PREDICTION RESULTS '''
    saveResult(output_path+"masks/", results)
    K.clear_session()
    image = cv2.imread("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/3_data.jpg")
    h, w, c = image.shape
    # print('width:  ', w)
    # print('height: ', h)
    # print('channel:', c)


    y = 0
    x = 0
    h = h
    w = w
    crop_image = image[x:w, y:h]
    cv2.imwrite("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/3_data.jpg", crop_image)

    '''----------------------------------------'''
    sw_lat = bounds['_southWest']['lat']
    # print(sw_lat)
    sw_long = bounds['_southWest']['lng']
    # print(sw_long)
    ne_lat = bounds['_northEast']['lat']
    # print(ne_lat)
    ne_long = bounds['_northEast']['lng']
    # print(ne_long)
    southwest = [str(sw_lat), str(sw_long)]

    # print(southwest)
    northeast = [str(ne_lat), str(ne_long)]
    # print(northeast)
    path1="/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads01/"
    get1="3_data.jpg"
    gdal_convert(path1,get1,southwest,northeast)
    # geojson5()


    with open("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/tiff_image/3_data.tif", "rb") as r1:
        converted_string = base64.b64encode(r1.read())
    #

    img = cv2.imread("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads02/masks/0_predict.png")
    #print(img)
    resized_img = cv2.resize(img,(1595,785))
    cv2.imwrite("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads02/masks/0_predict.png", resized_img)
    with open("/mnt/vol2/Dhruv_Raghav/general_unet_model/Api_deploy/uploads02/masks/0_predict.png", "rb") as r2:
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

    url = 'http://10.10.21.227:7005/satellite_model/'
    files = [('file', (filename, static_file.read(), content_type)), ('mask', mask)]
    #print("files", files)
    # values["geotag"] = request.form['geotag']
    #print("geotag", values)
    # values["scale"] = request.form['scale']
    # values["img_type"] = request.form['img_type']
    values["mask"] = mask

    headers = {}
    r = requests.request("POST", url, files=files, data=values, headers=headers)
    if r.status_code == 200:

        return json.loads(r.text)
    else:
        return json.loads(
            '{"error": "Something went wrong while processing image", "status_code": 500}'), 500







@app.route('/Habitation/',methods=['POST'])
def Habitation():
    print("Welcome to Habitation Detection:")
    resp=Response(status=200,content_type='application/json')
    image = request.files['file']  # Single image path
    # print("image",image)
    # image = request.files.get('file', '')

    # try:
    try:
        if(request.content_type!=None):
             if request.content_type.startswith('multipart/form-data'):
                 # print(request.content_type.startswith('multipart/form-data'))
                 if 'file' and 'bounds' in request.form.keys():




                    get1 = image.filename
                    # print("full file name",get1)
                    get2=image.filename.split('.')[1]
                    # print("extension", get2)
                    get3=image.filename.split('.')[0]
                    # print("filename",get3)

                    bounds = eval(request.form.get('bounds'))


                    if (get2 == 'tif' or get2 == 'jpg' or get2 == 'png' ):
                        # print("inside function 3")
                        resp=func3(image,get1,get3,bounds)
                        return resp
                    else:
                                    resp.status_code = 400
                                    return resp


                 else:
                    #print("invalid parameters")
                    resp.status_code = 400
                    return resp


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
    app.run(host='0.0.0.0', port=7011, debug=False)