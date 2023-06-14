'''
 Wrapper script defines a function called TSDR_Wrapper, which is the main function that is called to initiate the processing.
The function establishes a connection to a PostgreSQL database using psycopg2. It then repeatedly calls check_queue function,
which checks the database for new items to process. If a new item is found, the function calls initiate_tsdr function,
which begins the batch processing. initiate_tsdr first updates the proc_count of the GPU server in the database, indicating that a new task is being processed.
It then validates the path specified in w_path by calling populate_v3.validate.

If the path is valid, it adds a new task to the database using populate_v3.add_task and calls zebra_detect_v1.detect_batch to process the images in the specified folder.
If the validation fails, initiate_tsdr updates the remark column of the database entry to reflect the failure.
The script also defines a handler object for logging and sets the logging level to INFO.
 Finally, the script defines several global variables, including timing, Model_name, and proc_count.
'''


from datetime import datetime
import time
import populate_v3
import zebra_detect_v1

import psycopg2
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
#from api.detect_batch_v3 import detect_batch
# from celery.task.control import revoke
#from celery.worker.control import revoke
from PIL import Image
# from celery import Celery
# from celery_conf import app
#import datetime




import pandas as pd
import os

batch_connect2 = "dbname='ai_ml_hub' user='postgres' host='10.1.1.123' " + "password='postgres'"
batch_connect = "dbname='brand' user='postgres' host='10.1.1.123' " + "password='postgres'"
# batch_connect2 = "dbname='ai_ml_hub' user='postgres' host='10.1.1.123' " + "password='postgres'"
# batch_connect = "dbname='tsdr' user='postgres' host='10.1.1.123' " + "password='postgres'"


handler = TimedRotatingFileHandler('Logs/log-traffic', when='MIDNIGHT', backupCount=7)


formatter = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

# formatter_batch = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

logger = logging.getLogger('werkzeug')

handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.propagate = False



# class TSDR_Wrapper:
timing=100
Model_name='brand'
proc_count=1

def TSDR_Wrapper():
    conn = psycopg2.connect(batch_connect2)
    cursor = conn.cursor()
    cursor.execute("select server_name from catalog.model_server_info where model_name='{model}'".format(model=Model_name))
    server_name=cursor.fetchone()[0]
    print(server_name)
    while True:
        # print("check", datetime.now().strftime("%H:%M:%S"))
        check_queue(server_name,cursor)
        conn.commit()
        time.sleep(timing)

def check_queue(server,cursor):
    try:
        cursor.execute("select proc_count from catalog.gpu_server_info where server_name='{server}'".format(
                        server=server))
        server_count=cursor.fetchone()[0]
        if(server_count<proc_count):
            print("checked", datetime.now())
            cursor.execute("select folder_path,state from catalog.process_queue where model_name='{model}' and state "
                           "in(0,2,3) order by datetime limit 1".format(model=Model_name))
            q_data=cursor.fetchone()
            if(q_data!=None):
                print("process found", q_data)
                initiate_tsdr(q_data[0],q_data[1])
        else:
            print("checked",datetime.now())

    except Exception as e:
        print(e)


def initiate_tsdr(w_path, state):
    try:
        conn1 = psycopg2.connect(batch_connect2)
        cursor1 = conn1.cursor()
        cursor1.execute("select server_name from catalog.model_server_info where model_name='brand'")
        server_name = cursor1.fetchone()[0]
        cursor1.execute(
            "update catalog.gpu_server_info set proc_count = proc_count+1 where server_name='{server}'".format(
                server=server_name))
        conn1.commit()
        conn1.close()
        path = w_path.replace('%20', ' ').replace('\\', '/').replace('//', '/').replace('/10.1.1.', '/mnt/10.1.1.')
        print(path)
        # path=w_path
        if not os.path.exists(path):
            logger.info(msg=f'Folder path not available for\t' + w_path)
            populate_v3.update_remark(w_path,'Folder path not available')

            # command='ls'
            # os.system(command)

        # Check if path exists in DB
        else:
            if state==0:
                Flag,route = populate_v3.validate(w_path,str(state))

                if(Flag==True):
                    populate_v3.add_task(w_path, route)
                    zebra_detect_v1.detect_batch(path,w_path, route)
                    # print(task.id)
                    logger.info(msg=f'Detecting Processing path \t' + path )
                    # populate_v3.add_task(w_path,route)
                else:
                    logger.info(msg=f'Invalid data for Processing path \t' + path)
                    populate_v3.update_remark(w_path, 'Invalid data for Processing')

            elif state==2:
                Flag, table_name, processed_items = populate_v3.validate(w_path, str(state))

                if (Flag == True):
                    task = zebra_detect_v1.detect_batch(path,w_path, table_name,processed_items)
                    # print(task.id)
                    logger.info(msg=f'Resuming Processing path \t' + path)
                    populate_v3.add_task(w_path, table_name)
                else:
                    logger.info(msg=f'Invalid data for Processing path \t' + path)
                    populate_v3.update_remark(w_path, 'Invalid data for Processing')


            elif state==3:
                Flag, table_name = populate_v3.validate(w_path,str(state))

                if (Flag == True):
                    task = zebra_detect_v1.detect_batch(path,w_path, table_name)
                    # print(task.id)
                    logger.info(msg=f'Detecting Processing path \t' + path)
                    populate_v3.add_task(w_path, table_name)
                else:
                    logger.info(msg=f'Invalid data for Processing path \t' + path)
                    populate_v3.update_remark(w_path, 'Invalid data for Processing')
            else:
                logger.info(msg=f'Invalid data for Processing path \t' + path)
                populate_v3.update_remark(w_path, 'Invalid data for Processing')
    except Exception as e:
        logger.error(
            msg='Exception occurred\t' + str(e) + '\tTraceback\t' + '~'.join(
                str(traceback.format_exc()).split('\n')))
        populate_v3.update_remark(w_path, str(e))

if __name__ == '__main__':
    TSDR_Wrapper()
