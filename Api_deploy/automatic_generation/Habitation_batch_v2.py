import base64
import time
import cv2
import requests
import torch
from tab_file import tab,tab_2
# from Api_deploy.gdal_convert import gdal_convert, gdal_convert_01
from data import  testGenerator_01, saveResult_01, saveResult
from model import unet
from keras import backend as K
import tensorflow as tf
import csv
import GPUtil
import os
import sqlite3
import geopandas as gpd
import json
import psycopg2

batch_connect = "dbname='Habitation' user='postgres' host='10.1.1.123' " + "password='postgres'"
batch_connect2 = "dbname='ai_ml_hub' user='postgres' host='10.1.1.123' " + "password='postgres'"


with tf.Session() as sess:
    # Get the default graph
    graph = tf.get_default_graph()
    # Print all tensors in the graph
    for tensor in graph.as_graph_def().node:
        print(tensor.name)

def image_to_grey_sort_resize(input_path,dest_path2,file):
    input_path =input_path
    dest_path2 = dest_path2
    # reading the image
    try:
        # image = Image.open(input_path)
        img = cv2.imrea
        d(input_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray_image = image.convert('L')
        resized_img = cv2.resize(gray, (512, 512))
        # resized_img.save(dest_path2 + '/' + str(count) + ".png")
        cv2.imwrite(dest_path2 , resized_img)

    except Exception as e:
        print("Error converting image to gray scale:", e)






# def run_model():
#
#     return model


def clear_gpu_memory():
    import tensorflow as tf

    tf.reset_default_graph()

'''============================================'''


def create_shapefile(geojson_file, shapefile_name):
    try:
        # Load geojson file into a GeoDataFrame
        gdf = gpd.read_file(geojson_file)

        # Write GeoDataFrame to shapefile
        gdf.to_file(shapefile_name, driver="ESRI Shapefile")
        print(f"Shapefile created successfully: {shapefile_name}")

    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print(f"Error: Geojson file not found: {geojson_file}")
        elif isinstance(e, json.JSONDecodeError):
            print(f"Error: Invalid geojson file: {geojson_file}")
        else:
            print(f"Error: {e}")





'''-----------------------------------------------------------'''
# def create_db(db_name):
#     conn = sqlite3.connect(db_name)
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS image_geojson (image_name text, geojson text)''')
#     conn.commit()
#     conn.close()

def habitation_batch(src_folder,dst_folder,table_name):


    # print('in batch process',table_name)

    # list to store the names of the processed images
    try:
        conn = psycopg2.connect(batch_connect)
        cursor = conn.cursor()
    except Exception as e:
        print(str(e))
        return str(e)
    try:
        # print('process_started')
        processed_images = []
        # get the list of files in the source folder
        files = os.listdir(src_folder)
        files.sort()
        print(files)
        # print("select distinct image_name from {table}".format(table=table_name))

        cursor.execute("select distinct image_name from {table}".format(table=table_name))
        img_data = cursor.fetchall()
        for img_d in img_data:
            processed_images.append(img_d[0])

        print(processed_images)

        for file in files:
            # get the file path
            file_path = os.path.join(src_folder, file)
            # print(file)
            # check if the file is an image and not already processed
            if (file.endswith(".jpg") or file.endswith(".png")) and file not in processed_images:
                # get the corresponding tab file
                tab_file = file.replace(".jpg", ".TAB").replace(".png", ".TAB")
                tab_file_path = os.path.join(src_folder, tab_file)
                values = {}


                # check if the tab file exists
                if os.path.exists(tab_file_path):
                    try:
                        # convert the image to gray scale
                        file1 = file.split(".")[0]
                        print(tab_file_path)
                        w1, w2, h1, h2 = tab_2(tab_file_path)
                        file3 = file.split(".")[1]
                        # print(file_path)
                        new_img = cv2.imread(file_path)
                        # print(new_img.shape)
                        # print(file1)
                        # print(file3)
                        # print(new_img)
                        # cv2.imwrite(dst_folder + file1 + '1' + '.' + file3, new_img)

                        new_img1 = new_img[h1:h2, w1:w2]
                        # print(dst_folder + file1 + '.' + file3)
                        cv2.imwrite(dst_folder + file1 + '.' + file3, new_img1)
                        h=h2-h1
                        w=w2-w1
                        # print('saved')
                        image_path = dst_folder + file1 + '.' + file3
                        mask_path = dst_folder + file1 + '_mask.png'


                        gray_image_path = os.path.join(dst_folder, file1+'_gray.jpg')

                        count = image_to_grey_sort_resize(image_path, gray_image_path,file)

                        count=1
                        num_images = count
                        # print("count", count)

                        gray_file=file1+'_gray.jpg'


                        testGene = testGenerator_01(gray_file,dst_folder,num_image=num_images, target_size=(512, 512))

                        model = unet()

                        model.load_weights(
                            "/mnt/vol1/PycharmProjects/Habitation_Segmentation/weights/hatitat_final.hdf5")
                        # print('model loaded')
                        results = model.predict_generator(testGene, num_images, verbose=1)




                        #
                        # try:
                        #     os.makedirs(path_mask, exist_ok=True)
                        # except OSError as error:
                        #     pass
                        # print('prediction done')
                        # saveResult(file,dst_folder, results, w, h)
                        # print('result saved')
                        # saveResult(dst_folder, results)
                        saveResult_01(file,dst_folder, results)


                        resp = tab(tab_file_path)
                        # print("resp", resp)
                        bounds=resp["bounds"]


                        K.clear_session()

                        sw_lat = bounds['_southWest']['lat']
                        sw_long = bounds['_southWest']['lng']
                        ne_lat = bounds['_northEast']['lat']
                        ne_long = bounds['_northEast']['lng']
                        southwest = [str(sw_lat), str(sw_long)]
                        # print("southwest",southwest)

                        northeast = [str(ne_lat), str(ne_long)]
                        values = {}

                        url = 'http://10.1.1.130:7009/satellite_tiff/'
                        # dst_folder2=dst_folder.replace('vol2','10.1.1.130')
                        values["file_name"] = dst_folder + file1
                        values["ulx"] = southwest[1]
                        values["uly"] = northeast[0]
                        values["lrx"] = northeast[1]
                        values["lry"] = southwest[0]
                        # print(url)
                        # print(values)

                        res = requests.request("POST", url, data=values, headers={})
                        # data=json.load(res.text)
                        # print(res.json())
                        # d = json.loads(res.json())

                        with open(dst_folder + file1 + '.geojson') as f:
                            data = f.read()
                            # print(data)

                        # insert_data("image_geojson.db", file, r.text)

                        # print('''INSERT INTO {table}(image_name,geo_data) VALUES ('{img}','{geo_data}')'''.format(table=table_name,
                        #                                                                           img=file,
                        #                                                                           geo_data=data))

                        cursor.execute('''INSERT INTO {table}(image_name,class,bbox) VALUES ('{img}','{geo_data}')'''.format(table=table_name,
                                                                                                  img=file,
                                                                                                  geo_data=data))

                        # insert_data(table_name, file, r.text)
                        # print("geojson with its name stored in database")

                        processed_images.append(file)

                        # print(retrieve_data("image_geojson.db"))
                        # print(retrieve_data_01("image_geojson.db", file))

                        #
                        # input_file = path_geojson + "/" + file.split(".")[0] + '.geojson'
                        # output_file = path_geojson + "/" + file.split(".")[0] + '.shp'
                        #
                        # # ogr2ogr_cmd = f"ogr2ogr -f 'ESRI Shapefile' {output_file} {input_file}"
                        # #
                        # # subprocess.run(ogr2ogr_cmd, shell=True, check=True)
                        #
                        # # os.remove(path_geojson + "/" + file.split(".")[0] + ".dbf")
                        # # os.remove(path_geojson + "/" + file.split(".")[0] + ".prj")
                        # # os.remove(path_geojson + "/" + file.split(".")[0] + ".shx")
                        # geojson_file = input_file
                        # shapefile_name = output_file
                        # # Create shapefile
                        # create_shapefile(geojson_file, shapefile_name)


                        tf.keras.backend.clear_session()
                        os.remove(dst_folder + file.split(".")[0] + '_gray.jpg')
                        os.remove(dst_folder + file.split(".")[0] + '.tif')
                        os.remove(dst_folder + file.split(".")[0] + '.jpg')
                        os.remove(dst_folder + file.split(".")[0] + '_mask.png')

                        # update the list of existing files
                    except Exception as e:
                        print(str(e))
                        cursor.execute("INSERT INTO {table}(image_name,remark) VALUES ('{img}','{remark}')".format(
                            table=table_name,
                            img=file,
                            remark='Error Occured'))
                        print(file_path, 'Error')

                else:
                    cursor.execute("INSERT INTO {table}(image_name,remark) VALUES ('{img}','{remark}')".format(table=table_name,
                                                                                              img=file,
                                                                                              remark='Tab file not available'))

                cursor.execute("update catalog.folder_path_info set processed_count=processed_count+1 where route='{table}'".format(
                    table=table_name.lower()))
                conn.commit()
                # os.remove(dst_folder + file.split(".")[0] + '_mask.png')

        existing_files = files
        cursor.execute("update catalog.folder_path_info set state=3 where route='{table}'".format(
            table=table_name.lower()))
        conn.commit()
        # del model
        return 'Success'


    except Exception as e:
        # print('DB connection not established')
        print(e)
        # if (model != None):
        #     del model
        return str(e)
    #

if __name__ == '__main__':
    # src_folder = "/mnt/vol2/dhruv_raghav/2023/transfer/Sample_data/"
    # # # folder to save the gray scale images
    # dst_folder = "/mnt/vol2/dhruv_raghav/2023/transfer/results/"

    habitation_batch('/mnt/10.1.1.35/survey_placed_images/test/state_test/','/mnt/10.1.1.35/survey_placed_images/test/results/','hsurvey_placed_images_test_state_test_20230309')
