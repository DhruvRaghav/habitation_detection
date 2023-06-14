import json
import requests
from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/habitation_detection', methods=['POST'])
def satellite_FP_1():

    values = {}
    if request.method == 'POST':
        if 'file' and 'geotag' and 'scale' and 'img_type' in request.form.keys():
            #print(request)
            static_file = request.files['file']

            filename = static_file.filename

            content_type = static_file.content_type
            url = 'http://10.10.21.159:6003/Habitation'

            files = [('file', (filename, static_file.read(), content_type))]
            values["geotag"]= request.form['geotag']
            values["scale"] = request.form['scale']
            values["img_type"] = request.form['img_type']
            print(values)
            headers = {}
            filename1 = filename.split('.')[1]
            filename1 = filename1.lower()
            print('file', filename1)
            if (filename1 == "tiff" or filename1 == "tif") and values["geotag"] == "1" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)
                else:
                    return json.loads(
                        '{"error": "Something went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "0" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)

                else:
                    return json.loads(
                        '{"error": "Somethin;g went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "2" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                if 'bounds' in request.form.keys():
                    values["bounds"]= request.form['bounds']
                    r = requests.request("POST", url, files=files, data=values, headers=headers)
                    if r.status_code == 200:
                        return json.loads(r.text)
                    else:
                        return json.loads('{"error": "Something went wrong while processing image", "status_code": 500}'), 500
                else:
                    return json.loads(
                        '{"error": "Image Bounds Required", "status_code": 500}'), 500
            else:
                return json.loads('{"error": "Invalid parameter values", "status_code": 500}'), 500

        else:
            return json.loads('{"error": "Invalid Inputs parameters", "status_code": 500}'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
