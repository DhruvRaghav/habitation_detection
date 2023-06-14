import ast
import json
import logging
import os
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

import requests
from flask import Flask, request, Response
app = Flask(__name__)

import datetime

if not (os.path.exists('Logs')):
    os.makedirs('Logs/',exist_ok=False)
log_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
handler = TimedRotatingFileHandler('Logs/'+log_filename, when='MIDNIGHT', backupCount=7)

formatter = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

logger = logging.getLogger('gunicorn.error')

handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.setLevel(logger.level)
logger.addHandler(handler)

logger.propagate = False
from flask_cors import CORS

@app.before_request
def verify_asset():
    resp = Response(status=200, content_type='application/json')

    if 'authorization' in request.headers:
        pass
    else:
        return json.loads('{"code": "400","auth": "unsuccessful","error": "token parameter missing"}'), 400

    token = request.headers.get('authorization')
    # print(token)

    if len(token) != 0:

        try:
            token = str(token).lower().strip()
            if 'bearer' in token:
                token = token.replace('bearer ', '')

                assetid = 'ast1661851488i1868784548'

                ip = '127.0.0.1'

                domain = request.host

                url = "https://outpost.mapmyindia.com/api/security/oauth/check_token?token=" + token + "&api=" + assetid + "&ip=" + ip + "&domain=" + domain

                payload = {}
                files = {}
                headers = {
                    'Authorization': 'Basic '
                                     'c0sySUxhcF9fcC03d2xtaGZjdGhiM01IMkN1OENQdmV2V0k4UjlnOUZKS1hETDFBQ05GLVM4NEFtdi1uNDJUd'
                                     'FZLaVB6SHhoZmxtQ0dURExSSFhvQlE9PTp0TThpUlZwRkp6VHdlaFltY2JWVjJMNzk2QzhSNTBvZGMtWUd2S'
                                     'khnaV9PeUY3QkhZZjg1RVFra3MzZ21tZi0weWdDVV96ZjNOSDY2Qzc2RktnR1Iwb3dyYWpxOGNpcVQ= '
                }

                response = requests.request("GET", url, headers=headers, data=payload, files=files)

                if response.status_code != 200:
                    resp.status_code = 401
                    resp.data = json.dumps({"code": "401",
                                            "auth": "unsuccessful",
                                            "error": "access denied"})
                    return resp

                else:
                    print('token verified')

            else:
                resp.status_code = 401
                resp.data = json.dumps({"code": "401",
                                        "auth": "unsuccessful",
                                        "error": "Invalid Token Access Denied"})
                return resp

        except Exception as e:
            print(e)
            resp.status_code = 401
            resp.data = json.dumps({"code": "401",
                                    "auth": "unsuccessful",
                                    "error": "error while verifying token \n" + str(e)})
            return resp
    else:
        resp.status_code = 400
        resp.data = json.dumps({"code": "400",
                                "auth": "unsuccessful",
                                "error": "empty token parameter"})
        return resp

# from flask import Flask, jsonify
# from flask_cors import CORS, cross_origin
#
# app = Flask(__name__)
# CORS(app, support_credentials=True)



def application(environ, start_response):
  if environ['REQUEST_METHOD'] == 'OPTIONS':
    start_response(
      '200 OK',
      [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
        ('Access-Control-Allow-Methods', 'POST'),
      ]
    )
    return ''
@app.route('/Habitation/', methods=['POST'])
# @cross_origin(supports_credentials=True)

def habitation():
    c={}
    values = {}
    resp=Response(status=200,content_type='application/json')


    try:
        if(request.content_type!=None):
            if request.method == 'POST':
              if request.content_type.startswith('multipart/form-data'):
                if 'file' and 'bounds' in request.form.keys():

                    c["bounds"] = request.form['bounds']
                    print("The original string : " + str(c["bounds"]))
                    # c["bounds"]= "'"+ c["bounds"] + "'"
                    # print("dadsd",c["bounds"])

                    # using json.loads()
                    # convert dictionary string to dictionary
                    # res = json.loads(c["bounds"])
                    d = ast.literal_eval(c["bounds"])
                    # print result
                    print("The converted dictionary : " ,(d))
                    print(type((d)))
                    '''---------------------'''

                    list = []
                    for element in d.keys():
                        print(element)
                        print(type(element))
                        list.append(element)
                    if list[0] == "_southWest" and list[1] == "_northEast":
                        print("helo")

                        # if (type(element['lat']))
                    list = []
                    for element in d.values():
                        list.append(element)
                    # print("list", list)

                    # print(list[1]['lat'])

                    if (list[0]['lat'] != None) and (list[0]['lng'] != None) and (list[1]['lng'] != None) and (
                            list[1]['lat'] != None):
                        # print(list[0]['lat'])
                        if type(list[0]['lat']) == float and type(list[0]['lng']) == float and type(
                                list[1]['lng']) == float and type(list[1]['lat']) == float:

                            # print("1")

                            print(request.files)


                            if(len(request.files))==0:
                                return json.loads('{"error": "Invalid Inputs parameters", "status_code": 400}'), 400

                            static_file = request.files['file']
                            filename = static_file.filename
                            if filename=='':
                                return json.loads('{"error": "Invalid Inputs parameters", "status_code": 400}'), 400


                            content_type = static_file.content_type
                            url = 'http://10.10.21.159:7012/Habitation/'

                            files = [('file', (filename, static_file.read(), content_type))]
                            # values["geotag"]= request.form['geotag']
                            # values["scale"] = request.form['scale']
                            # values["img_type"] = request.form['img_type']
                            #print(values)

                            headers = {}
                            filename1 = filename.split('.')[1]
                            filename1 = filename1.lower()
                            print('file', filename1)

                            if (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") :
                                if 'bounds' in request.form.keys():
                                    values["bounds"]= request.form['bounds']
                                    r = requests.request("POST", url, files=files, data=values, headers=headers)
                                    if r.status_code == 200:
                                        return json.loads(r.text)
                                    else:
                                        return json.loads('{"error": "Something went wrong while processing image", "status_code": 500}'), 500
                                else:
                                    return json.loads(
                                        '{"error": "Image Bounds Required", "status_code": 500}'), 400
                            else:
                                return json.loads('{"error": "Invalid parameter values", "status_code": 500}'), 400

                        else:
                            return json.loads('{"error": "Invalid parameter values", "status_code": 400}'), 400

                    else :
                        return json.loads('{"error": "Enter the parameters", "status_code": 400}'), 400


                else:
                    return json.loads('{"error": "Invalid Inputs parameters", "status_code": 400}'), 400
              else:
                  return json.loads('{"error": "Invalid Inputs parameters", "status_code": 400}'), 400


            else:
                resp.status_code = 400
                return json.loads('{"error": "Invalid Inputs parameters", "status_code": 400}'), 400
        else:
            resp.status_code = 400
            return json.loads('{"error": "Invalid Inputs parameters", "status_code": 400}'), 400
    except Exception as e:
        logger.error(msg=str(e),status_code=500)
        resp.status_code=500
        print(e)

        return resp



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6003, debug=False)