import time
import cv2
import torch
from data import  testGenerator_01, saveResult_01
from model import unet
import tensorflow as tf
import GPUtil
import os
import sqlite3
import geopandas as gpd
import json
import psycopg2
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
        file1 = file.split(".")[0]

        cv2.imwrite(dest_path2+"/"+file1+".jpg" , resized_img)

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
    src_folder = "/home/ceinfo/Desktop/sat_test_data_1/"
    # folder to save the gray scale images
    dst_folder = "/home/ceinfo/Desktop/sat_test_data_mask/"
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
    model = run_model()
    while True:
        try:
            # get the list of files in the source folder
            files = os.listdir(src_folder)
            # loop through the new files that have been added
            for file in set(files) - set(existing_files):
                # get the file path
                file_path = os.path.join(src_folder, file)
                # print(file)
                # check if the file is an image and not already processed
                if (file.endswith(".jpg") or file.endswith(".png")) and file not in processed_images:
                    '''--------------------------------------------------------------------------------'''
                    '''PREPROCESSING TESTING IMAGE'''
                    gray_image_path = os.path.join(dst_folder, file)

                    count = image_to_grey_sort_resize(file_path, dst_folder,file)

                    count=1
                    num_images = count
                    '''--------------------------------------------------------------------------------'''
                    ''' testing starts here '''
                    # perform inference

                    data_gen = testGenerator_01(file,dst_folder, num_image=num_images, target_size=(512, 512))
                    with torch.no_grad():
                        # model.eval()
                        results = model.predict_generator(data_gen, steps=1)

                    '''The torch.no_grad() context manager is used to turn off gradient calculations during model
                     inference, which can help to reduce memory usage and speed up computation. The model.predict_generator()
                     method is used to generate predictions on the data_gen dataset in batches, with the steps argument specifying 
                     the number of batches to generate predictions on. It's worth noting that the model must be
                      previously trained and loaded into memory for this code to work. 
                     Additionally, the model.eval() method is commented out in this code snippet, but it is typically used to 
                     set the model to evaluation mode, which can affect certain layers like dropout and batch normalization.'''

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
                    clear_gpu_memory()
                    existing_files = files
        except Exception as e:
                    print("Error reading the source folder:", e)

                # wait for 1 second before checking for new files again
        time.sleep(20)

if __name__ == '__main__':
    auto_habitation_detection()