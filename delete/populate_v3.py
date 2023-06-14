import os
import shutil
import psycopg2
import json
from _datetime import datetime, timedelta, date
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
import pandas as pd
import ast
import re


os.makedirs('./Logs/DBLogs/', exist_ok=True)

logger = logging.getLogger('__name__')
log_filename = 'log-populate'
handler = TimedRotatingFileHandler('Logs/DBLogs/' + log_filename, when='MIDNIGHT', backupCount=7)
formatter = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.propagate = False

# batch_connect = "dbname='tsdr' user='postgres' host='10.1.1.123' " + "password='postgres'"
# batch_connect2 = "dbname='ai_ml_hub' user='postgres' host='10.1.1.123' " + "password='postgres'"
batch_connect = "dbname='urm_1' user='postgres' host='10.1.1.123' " + "password='postgres'"
batch_connect2 = "dbname='ai_ml_hub' user='postgres' host='10.1.1.123' " + "password='postgres'"
# batch_connect = "dbname='ce_info' user='postgres' host='10.1.1.168' " + "password='postgres'"


# batch_connect = "dbname='tsdr' user='postgres' host='10.1.1.123' " + "password='postgres'"

def validate(path, state):
    """
    Function to check if path already exists in folder_path_nfo
    If yes, return the details
    :param path: Path to be checked
    :param need: Type of object to be detected
    :return:
    exists : True/False if path exists or not
    s_no: Serial number of the path entry in folder_path_info
    processed_items: Number of images tha have been processed
    total_items: Total images in path
    state: Current process state. 1 - processing / 2 - interrupted / 3 - completed
    valid_state: Current validation state. 1 - Validating / 2 - interrupted / 3 - completed
    valid_count: Number of images validated
    """
    try:

        conn = psycopg2.connect(batch_connect)
        cursor = conn.cursor()

        if(state=='0'):
            cursor.execute("SELECT ROUTE, STATE FROM catalog.folder_path_info WHERE folder_path='{path}'"
                            .format(path=path))
            data = cursor.fetchone()
            if(data is None):
                route=add_path(path,cursor,conn)
                return True,route
            else:
                return False,data[1]

        elif (state == '2'):
            cursor.execute("SELECT ROUTE, PROCESSED_COUNT, STATE FROM catalog.folder_path_info WHERE folder_path='{path}'".
                           format(path=path))
            data = cursor.fetchone()
            if(data is None):
                return False,"Path not available to resume","a"

            elif(data[2]==2):
                cursor.execute("UPDATE catalog.folder_path_info SET state=1 WHERE route='{route}'".format(route=data[0],
                 date1=date.today()))
                conn.commit()

                return True,data[0],data[1]

            else:
                return False,'Unable to resume process','a'

        elif (state == '3'):
            cursor.execute("SELECT ROUTE, PROCESSED_COUNT, STATE, REQ_STAT FROM catalog.folder_path_info WHERE "
                           "folder_path='{path}' order by req_stat desc limit 1".format(path=path))
            data = cursor.fetchone()
            if (data is None):
                return False, "Path not available to reprocess"

            elif (data[2] == 2 or data[2] == 3):
                reprocess_path(path,data,cursor,conn)
                return True, data[0]

            else:
                return False, 'Unable to re-process'

        else:
            return False, "Error occured"


    except Exception as e:
        logger.error(
            msg='Exception occurred\t' + str(e) + '\tTraceback\t' + '~'.join(str(traceback.format_exc()).split('\n')))
        conn = None
        print(e)
        raise e

    # finally:
    #     if conn:
    #         conn.close()
    #         #return False, "Error occured"

def update_path(table_name, path):
    """
    Function to truncate a path table when re-processing complete path
    :param table_name: Table name
    :param need: Type of object required
    :return:
    None
    """
    try:
        conn = psycopg2.connect(batch_connect)
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE {table_name}".format(table_name=table_name))
        cursor.execute("UPDATE catalog.folder_path_info SET date_time='{date1}', processed_count=0, state=0 WHERE "+
                        "folder_path='{path}'".format(path=path,date1=date.today()))
        conn.commit()
        conn.close()
        return
    except Exception as e:
        logger.error(
            msg='Exception occurred\t' + str(e) + '\tTraceback\t' + '~'.join(str(traceback.format_exc()).split('\n')))

        raise e


def add_path(path,cursor,conn):
    """
    Function to truncate a path table when re-processing complete path
    :param table_name: Table name
    :param need: Type of object required
    :return:
    None
    """
    try:
        conn2 = psycopg2.connect(batch_connect2)
        cursor2 = conn2.cursor()
        route = path.split('Advanced_Car_Survey\\')[-1].replace('Raw_Input\\', '')
        route=route.replace('Image\\', '').replace('\\', '_').replace('.','').lower()
        route = route.replace('data_for_extraction_', '')
        route = route.replace('rvs_acs_', '')
        route = route.replace('acs_', '')
        route = route.replace('survey_', '')
        print(route)
        print("**********************{inside populate_v3.add_path_func}**************************")
        # route=path.split("\\")[-6]+'_'+path.split("\\")[-3]+'_'+path.split("\\")[-1]
        # route =path.split("/")[-3]+'_'+path.split("/")[-1]
        # route=route.lower()
        # path1=path
        path1=path.replace('%20', ' ').replace('\\', '/').replace('//', '/').replace('/10.1.1.', '/mnt/10.1.1.')
        server_name = path.split('\\')[1] + r'\\' + path.split('\\')[2]
        cursor2.execute("select server_path,published_path from catalog.path_server_mapping where server_path LIKE '%{server_name}%'".format(
                server_name=server_name))
        data = cursor2.fetchone()
        server = data[0]
        publish = data[1]
        print(server, publish)
        publish_path = path.replace(server, publish).replace('%20', ' ').replace('\\', '/')
        print(publish_path)

        try:
            cursor.execute('''insert into catalog.folder_path_info (date_time, folder_path, processed_count, total_count, state, 
                            published_path,route, req_stat) values('{date1}','{path}',0,{total_count},1,'{publish_path}','{route}',1)'''.
                           format(path=path, date1=str(date.today()), total_count=len(os.listdir(path1)),
                                  route=route.lower(), publish_path=publish_path))
            conn.commit()
            cursor.execute('''CREATE TABLE if not exists {route} (image_name text,box text,label text,lat double precision, 
                                        long double precision,timing time,heading double precision,description text, sign_type text,
                                        detection text,recognition text,view text,digitization text,new_description text, new_sign_type 
                                        text,edge_id integer,remarks text)'''.format(route=route.lower()))
            conn.commit()
        except Exception as e:
            print(e)
            conn.close()
            conn = psycopg2.connect(batch_connect)
            cursor = conn.cursor()
            route1 = path.split("\\")[-7] + '_' + path.split("\\")[-3] + '_' + path.split("\\")[-1]
            # route =path.split("/")[-3]+'_'+path.split("/")[-1]
            route1 = route1.lower()
            print('''CREATE TABLE if not exists {route} (image_name text,box text,label text,lat double precision, 
                                                    long double precision,timing time,heading double precision,description text, sign_type text,
                                                    detection text,recognition text,view text,digitization text,new_description text, new_sign_type 
                                                    text,edge_id integer,remarks text)'''.format(route=route1))
            cursor.execute('''CREATE TABLE if not exists {route1} (image_name text,box text,label text,lat double precision, 
                                        long double precision,timing time,heading double precision,description text, sign_type text,
                                        detection text,recognition text,view text,digitization text,new_description text, new_sign_type 
                                        text,edge_id integer,remarks text)'''.format(route1=route1))
            cursor.execute("update catalog.folder_path_info set route = '{route}' where folder_path='{path}'".
                           format(path=path,route=route1))
            conn.commit()
            route=route1
        print(route)
        return route
    except Exception as e:
        logger.error(
            msg='Exception occurred\t' + str(e) + '\tTraceback\t' + '~'.join(str(traceback.format_exc()).split('\n')))

        raise e


def add_task(path,task_id):
    try:
        conn = psycopg2.connect(batch_connect)
        cursor = conn.cursor()

        cursor.execute("insert into catalog.task_details values('{path}','{task_id}')".format(path=path,task_id=task_id))
        conn.commit()

        conn1 = psycopg2.connect(batch_connect2)
        cursor1 = conn1.cursor()
        cursor1.execute("delete from catalog.process_queue where folder_path='{folder_path}' and model_name='urm_1'".format(
                folder_path=path))
        conn1.commit()
        conn1.close()
        conn.close()

    except Exception as e:
        logger.error(
            msg='Exception occurred\t' + str(e) + '\tTraceback\t' + '~'.join(str(traceback.format_exc()).split('\n')))

        raise e



def stop_batch(task_id):
    try:
        conn = psycopg2.connect(batch_connect)
        cur = conn.cursor()
        cur.execute("select folder_path from catalog.task_details where task_id='{task_id}'".format(task_id=task_id))
        path=cur.fetchone()
        remove_task(path[0])
        cur.execute("update catalog.folder_path_info set state=2 where folder_path='{w_path}'".format(w_path=path[0]))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)


def remove_task(path,route):
    try:
        conn = psycopg2.connect(batch_connect)
        cursor = conn.cursor()

        cursor.execute("delete from catalog.task_details where folder_path='{path}'".format(path=path))
        # cursor.execute("update catalog.folder_path_info set published_path='{publish_path}' where route='{route}'".
        #                format(publish_path=publish_path,route=route))

        conn1 = psycopg2.connect(batch_connect2)
        cursor1 = conn1.cursor()
        cursor1.execute("select server_name from catalog.model_server_info where model_name='urm_1'")
        server_name = cursor1.fetchone()[0]
        cursor1.execute("select proc_count from catalog.gpu_server_info where server_name='{server}'".format(server=server_name))
        proc_count = cursor1.fetchone()[0]
        if(proc_count>0):
            cursor1.execute("update catalog.gpu_server_info set proc_count = proc_count-1 where server_name='{server}'".format(
                server=server_name))
        conn.commit()
        conn1.commit()
        conn1.close()
        conn.close()
    except Exception as e:
        logger.error(
            msg='Exception occurred\t' + str(e) + '\tTraceback\t' + '~'.join(str(traceback.format_exc()).split('\n')))

        raise e

def update_remark(path,msg):
    conn1 = psycopg2.connect(batch_connect2)
    cursor1 = conn1.cursor()
    cursor1.execute("update catalog.process_queue set state=4,remarks='{msg}' where folder_path='{w_path}'".
                    format(w_path=path,msg=msg))
    cursor1.execute("select server_name from catalog.model_server_info where model_name='urm_1'")
    server_name = cursor1.fetchone()[0]
    cursor1.execute("update catalog.gpu_server_info set proc_count = proc_count-1 where server_name='{server}'".format(
        server=server_name))
    conn1.commit()


def reprocess_path(path,data,cursor,conn):

    try:
        route = path.split('Advanced_Car_Survey\\')[-1].replace('Raw_Input\\', '')
        route = route.replace('Image\\', '').replace('\\', '_').replace('.', '').lower()
        route = route.replace('data_for_extraction_', '')
        route = route.replace('rvs_acs_', '')
        route = route.replace('survey_', '')
        print(route)
        print("ooooooooooooooooooooooooooooooooooooooooo[reprocess_func]ooooooooooooooooooooooooooooooooooooooooo")
        # route=path.split("\\")[-6]+'_'+path.split("\\")[-3]+'_'+path.split("\\")[-1]
        # route =path.split("/")[-3]+'_'+path.split("/")[-1]
        # route=route.lower()
        # path1=path
        new_name = data[0] + "_" + str(data[3])
        cursor.execute(
            '''Alter table if exists {route} rename to {new_name}'''.format(route=data[0], new_name=new_name))
        cursor.execute("Alter table if exists {new_name} set schema archive".format(new_name=new_name))
        path1=path.replace('%20', ' ').replace('\\', '/').replace(
            '//', '/').replace('/10.1.1.', '/mnt/10.1.1.')
        cursor.execute("update catalog.folder_path_info set route='{new_name}' where route='{route}'".format(
                           path=path, date1=date.today(), total_count=len(os.listdir(path1)), route=route.lower(),
                           r_stat=data[3] + 1,new_name=new_name))

        cursor.execute("insert into catalog.folder_path_info (date_time, folder_path, processed_count,"+
                        "total_count, state, route, req_stat) values('{date1}','{path}',0,{total_count},1,'{route}',{r_stat})".format(
                        path=path,date1=date.today(),total_count=len(os.listdir(path1)),route=route.lower(),r_stat=data[3]+1))

        cursor.execute('''CREATE TABLE {route} (image_name text,box text,label text,lat double precision, 
                        long double precision,timing time,heading double precision,description text, sign_type text,
                        detection text,recognition text,view text,digitization text,remarks text)'''.format(route=
                        route.lower()))
        conn.commit()
        return route
    except Exception as e:
        logger.error(
            msg='Exception occurred\t' + str(e) + '\tTraceback\t' + '~'.join(str(traceback.format_exc()).split('\n')))

        raise e

def update_publish_path(w_path):
    # "\\10.1.1.35\de04\NavigationSource\Advanced_Car_Survey\Assam\V19.1\MCC_Guwahati_Car2\Raw_Input\Data_for_Extraction\07032019\Image\F"
    # "http://10.1.1.76/img_de_04/NavigationSource/Advanced_Car_Survey/Assam/V19.1/MCC_Guwahati_Car2/Raw_Input/Data_for_Extraction/07032019/Image/F"
    path_all=w_path.split('\\')
    print(path_all)


def update_edges(table_name):
    try:
        conn = psycopg2.connect(batch_connect)
        cur = conn.cursor()
        # conn2 = psycopg2.connect(batch_connect2)
        # cur2 = conn2.cursor()

        print("started :", datetime.now().strftime("%H:%M:%S"))
        cur.execute('''alter table {route} add column if not exists geom1 geometry(Point,4326)'''.format(route=table_name))
        cur.execute('''alter table {route} add column if not exists edge_id integer'''.format(route=table_name))
        cur.execute('''update {route} set geom1=st_setsrid(st_makepoint(long,lat),4326)'''.format(route=table_name))
        cur.execute('''create index if not exists {route}_geom on {route} using gist(geom1)'''.format(route=table_name))
        # conn.commit()
        print("index done :", datetime.now().strftime("%H:%M:%S"))
        cur.execute('''select distinct unique_id from sde.vt_grid a,{route} b where st_within(geom1,shape)=true'''.format(route=table_name))
        grids=cur.fetchall()
        print(grids)
        if(grids!=None):
            for grid in grids:
                # print(grid[0])
                cur.execute('''update {route} b set edge_id=(select a.edge_id from sde.{grid}_rd_net a
                             where st_dwithin(a.shape,b.geom1,0.0001)=true order by ST_DistanceSphere(a.shape,b.geom1) asc
                             fetch first 1 rows only) where edge_id is null'''.format(route=table_name,grid=grid[0]))
                # cur.execute('''select count(*) from traffic_sign_{route} where edge_id is not null'''.format(route=table_name, grid=grid[0]))
                # print(cur.fetchone())
                conn.commit()

                # print("mapmatching done for grid:",grid, datetime.now().strftime("%H:%M:%S"))
        cur.execute('''alter table {route} drop column geom1'''.format(route=table_name))
        conn.commit()
        conn.close()
        # conn2.close()
        return True
    except Exception as e:
        print(e)



def update_location(image_path,table):
    try:
        conn = psycopg2.connect(batch_connect)
        cur = conn.cursor()
        print("started :", datetime.now().strftime("%H:%M:%S"))
        side = image_path.split('/')[-1]
        print('side',side)
        try:
            if (side == 'L' or side == 'l'):
                view='Left'
                geo_csv = pd.read_csv(image_path.split('Image')[0] + 'Geocoded/MMISurvey.txt',
                                      names=['Time', '_', 'Latitude', 'Longitude', '_',
                                             '_', 'Angle', 'Left', '_', '_'],
                                      usecols=['Time', 'Latitude', 'Longitude', 'Angle', 'Left'])

            elif (side == 'F' or side == 'f'):
                view='Front'
                geo_csv = pd.read_csv(image_path.split('Image')[0] + 'Geocoded/MMISurvey.txt',
                                      names=['Time', '_', 'Latitude', 'Longitude', '_',
                                             '_', 'Angle', '_', 'Front', '_'],
                                      usecols=['Time', 'Latitude', 'Longitude', 'Angle', 'Front'])

            elif (side == 'R' or side == 'r'):
                view='Right'
                geo_csv = pd.read_csv(image_path.split('Image')[0] + 'Geocoded/MMISurvey.txt',
                                      names=['Time', '_', 'Latitude', 'Longitude', '_',
                                             '_', 'Angle', '_', '_', 'Right'],
                                      usecols=['Time', 'Latitude', 'Longitude', 'Angle', 'Right'])

            geo_csv[view] = geo_csv[view].str.split('/').str[-1]

        except Exception as e:
            if (side == 'L' or side == 'l'):
                geo_csv = pd.read_csv(image_path.split('Image')[0] + 'Geocoded/MMISurvey.txt',
                                      usecols=['Time', 'Latitude', 'Longitude', 'Angle', 'Left'])

            elif (side == 'F' or side == 'f'):
                geo_csv = pd.read_csv(image_path.split('Image')[0] + 'Geocoded/MMISurvey.txt',
                                      usecols=['Time', 'Latitude', 'Longitude', 'Angle', 'Front'])
            elif (side == 'R' or side == 'r'):
                geo_csv = pd.read_csv(image_path.split('Image')[0] + 'Geocoded/MMISurvey.txt',
                                      usecols=['Time', 'Latitude', 'Longitude', 'Angle', 'Right'])
            geo_csv[view] = geo_csv[view].str.split('\\').str[-1]


        cur.execute('select distinct image_name from {table} where lat=0'.format(table=table))
        image_data=cur.fetchall()
        print(image_data)
        for image in image_data:
            df = geo_csv[geo_csv[view] == image[0]]
            if not df.empty:
                timing, lat, long, heading = df['Time'].values[0], df['Latitude'].values[0], df['Longitude'].values[0], \
                                             df['Angle'].values[0]

                # print("update {table} set lat={lat},long={long},heading={head},timing='{time}' where image_name='{image}' ".format(table=table,
                #             lat=lat,long=long,head=heading,time=timing,image=image[0]))
                cur.execute("update {table} set lat={lat},long={long},heading={head},timing='{time}' where image_name='{image}' ".format(table=table,
                            lat=lat,long=long,head=heading,time=timing,image=image[0]))

            conn.commit()
        conn.close()
        # conn2.close()
        return True
    except Exception as e:
        print(e)

