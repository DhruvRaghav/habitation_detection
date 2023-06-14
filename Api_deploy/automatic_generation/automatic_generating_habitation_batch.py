import base64
import time
import cv2
import requests
import torch
from Api_deploy.automatic_generation.tab_file import tab
from Api_deploy.gdal_convert import gdal_convert, gdal_convert_01
from data import  testGenerator_01, saveResult_01
from model import unet
from keras import backend as K
import tensorflow as tf
import csv
import GPUtil
import os
import sqlite3
import geopandas as gpd
import json
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
        img = cv2.imread(input_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray_image = image.convert('L')
        resized_img = cv2.resize(gray, (512, 512))
        # resized_img.save(dest_path2 + '/' + str(count) + ".png")
        cv2.imwrite(dest_path2 , resized_img)

    except Exception as e:
        print("Error converting image to gray scale:", e)






def run_model():
    model = unet()

    model.load_weights("/mnt/vol2/Dhruv_Raghav/general_unet_model/weights/hatitat_final.hdf5")
    return model


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
def create_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS image_geojson (image_name text, geojson text)''')
    conn.commit()
    conn.close()

def insert_data(db_name, image_name, geojson):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO image_geojson VALUES (?,?)", (image_name, geojson))
    conn.commit()
    conn.close()

def retrieve_data(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM image_geojson")
    return c.fetchall()

def retrieve_data_01(db_name, column):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(f"SELECT {column} FROM image_geojson")
    return c.fetchall()

def auto_habitation_detection():


    # Get the GPU ID of the GPU being used by the current process
    pid = os.getpid()
    gpu_id = GPUtil.getFirstAvailable(order='memory', maxLoad=0.5, maxMemory=0.5)[0]

    # Get the GPU usage and memory usage
    gpu_load = GPUtil.getGPUs()[gpu_id].load * 100
    gpu_memory = GPUtil.getGPUs()[gpu_id].memoryUsed

    # Print the results
    print("GPU ID:", gpu_id)
    print("GPU Load: {:.2f}%".format(gpu_load))
    print("GPU Memory Used: {:.2f} MB".format(gpu_memory / (1024 * 1024)))
    tf.reset_default_graph()
    '''--------------------------------------------------------------------------------'''

    # folder to check for new images and tab files
    src_folder = "/home/ceinfo/Desktop/2023/"
    # folder to save the gray scale images
    dst_folder = "/home/ceinfo/Desktop/2023_result/"
    # list to store the names of the processed images
    processed_images = []
    # list to store the names of the files in the source folder
    existing_files = []
    '''--------------------------------------------------------------------------------'''

    folder = src_folder

    # Get a list of all files in the folder

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    # Sort the list of files
    files.sort()

    '''--------------------------------------------------------------------------------'''
    '''CREATE DATA BASE'''


    # Create the database
    create_db("image_geojson.db")

    while True:
        try:
            # get the list of files in the source folder
            files = os.listdir(src_folder)

            # loop through the new files that have been added
            #print("files",set(files))
            #print("existing",set(existing_files))

            for file in set(files) - set(existing_files):
                # get the file path
                file_path = os.path.join(src_folder, file)
                # print(file)
                # check if the file is an image and not already processed
                if (file.endswith(".jpg") or file.endswith(".png")) and file not in processed_images:
                    # get the corresponding tab file
                    tab_file = file.replace(".jpg", ".tab").replace(".png", ".tab")
                    tab_file_path = os.path.join(src_folder, tab_file)

                    # check if the tab file exists
                    if os.path.exists(tab_file_path):
                        # convert the image to gray scale

                        '''--------------------------------------------------------------------------------'''
                        '''PREPROCESSING TESTING IMAGE'''
                        gray_image_path = os.path.join(dst_folder, file)

                        count = image_to_grey_sort_resize(file_path, gray_image_path,file)

                        count=1
                        num_images = count
                        # print("count", count)



                        '''--------------------------------------------------------------------------------'''
                        ''' testing starts here '''

                        testGene = testGenerator_01(file,dst_folder,num_image=num_images, target_size=(512, 512))
                        model=run_model()
                        results = model.predict_generator(testGene, num_images, verbose=1)



                        '''--------------------------------------------------------------------------------'''
                        '''SAVING PREDICTION RESULTS '''
                        path = dst_folder
                        '''Directory'''
                        directory = "masks"
                        '''Parent Directory path'''
                        parent_dir = path
                        ''' Path'''
                        path_mask = os.path.join(parent_dir, directory)
                        # print("path1",path1)

                        '''Directory will be created at the current location of the project'''
                        try:
                            os.makedirs(path_mask, exist_ok=True)
                        except OSError as error:
                            pass

                        saveResult_01(file,path_mask+"/", results)

                        #saveResult(dst_folder + "/masks/", results)

                        '''--------------------------------------------------------------------------------'''
                        resp = tab(tab_file_path)
                        # print("resp", resp)
                        bounds=resp["bounds"]


                        '''--------------------------------------------------------------------------------'''
                        K.clear_session()
                        '''--------------------------------------------------------------------------------'''

                        sw_lat = bounds['_southWest']['lat']
                        sw_long = bounds['_southWest']['lng']
                        ne_lat = bounds['_northEast']['lat']
                        ne_long = bounds['_northEast']['lng']
                        southwest = [str(sw_lat), str(sw_long)]

                        northeast = [str(ne_lat), str(ne_long)]
                        # print("filepath ",file_path)
                        path1 = file_path
                        get1 = file

                        passage = gdal_convert_01(path1, get1, southwest, northeast)
                        # print("tiff file path ",passage)
                        file_1=file.split(".")[0] + ".tif"

                        with open(passage + "/" + file_1, "rb") as r1:
                            converted_string = base64.b64encode(r1.read())
                        #
                        # print("tiff file encoded")

                        img = cv2.imread(path_mask+"/" + file)

                        resized_img = cv2.resize(img, (1595, 785))

                        cv2.imwrite(path_mask+"/" + file, resized_img)
                        # print("mask reshaped")


                        with open(path_mask+"/" + file, "rb") as r2:
                            converted_string_1 = base64.b64encode(r2.read())
                        # print("mask encoded")

                        #os.remove(passage + "/" + file_1)

                        values = {}

                        mask = json.dumps(
                            {'T I F': converted_string.decode('utf-8'), 'M A S K': converted_string_1.decode(('utf-8'))})

                        url = 'http://10.10.21.228:7005/satellite_model/'





                        '''--------------------------------------------------------------------------------'''
                        files = [('file', (file, open(file_path, 'rb'), 'image/png')),('mask', mask)]
                        # print(files)
                        headers = {}
                        values["mask"] = mask
                        r = requests.request("POST", url, headers=headers, data=values, files=files)


                        #
                        os.remove(path_mask+"/" + file)
                        #os.remove(passage + "/" + file_1)
                        os.remove(dst_folder+file)



                        if r.status_code == 200:
                            processed_images.append(file)
                            d=json.loads(r.text)




                            '''--------------------------------------------------------------------------------'''
                            path = dst_folder
                            '''Directory'''
                            directory = "geojson"
                            '''Parent Directory path'''
                            parent_dir = path
                            ''' Path'''
                            path_geojson = os.path.join(parent_dir, directory)
                            # print("path1",path1)

                            '''Directory will be created at the current location of the project'''
                            try:
                                os.makedirs(path_geojson, exist_ok=True)
                            except OSError as error:
                                pass

                            '''--------------------------------------------------------------------------------'''

                            with open(path_geojson+"/" + file.split(".")[0]  + '.geojson', 'w') as fp:
                                 json.dump(d, fp)




                            '''**********************************************************************************'''
                            '''GEOJSON TO STORE IN DATABASE'''

                            insert_data("image_geojson.db",file,r.text)
                            print("geojson with its name stored in database")
                            # print(retrieve_data("image_geojson.db"))
                            # print(retrieve_data_01("image_geojson.db", file))

                            '''--------------------------------------------------------------------------------'''
                            # '''geojson to shape file '''
                            #
                            # input_file = path_geojson+"/" + file.split(".")[0]  + '.geojson'
                            # output_file = path_geojson+"/" + file.split(".")[0]  + '.shp'
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

                            '''--------------------------------------------------------------------------------'''

                            tf.keras.backend.clear_session()
                            clear_gpu_memory()
                            del model
                            torch.cuda.empty_cache()

                        else:
                            print("error while creating geojson")
                            clear_gpu_memory()
                            del model
                            torch.cuda.empty_cache()

                    else:
                        rows = [["NAME", "ERROR"]]
                        with open("data.csv", "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerows(rows)




                        entry=[tab_file, "Missing"]
                        # Open the CSV file in append mode
                        with open('data.csv','r', newline='') as f:
                            # Create a writer object

                            reader = csv.reader(f)
                            if [row for row in reader if row == entry]:

                                # entry already present, skip appending
                                pass

                            else:
                                with open('data.csv', 'a', newline='') as f:
                                    writer = csv.writer(f)
                                    # Add a new row of data to the CSV file
                                    writer.writerow(entry)



            # update the list of existing files
            existing_files = files
        except Exception as e:
            print("Error reading the source folder:", e)

        # print(retrieve_data("image_geojson.db"))
        # print(retrieve_data("image_geojson.db", "image_name"))
        # print(retrieve_data_01("image_geojson.db", file))
        # print(retrieve_data("image_geojson.db"))

        torch.cuda.empty_cache()
        clear_gpu_memory()

        # wait for 1 second before checking for new files again
        tf.reset_default_graph()

        time.sleep(1)



if __name__ == '__main__':
    auto_habitation_detection()