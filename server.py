import numpy as np
import collections
import pandas as pd
import threading
import time
from consts import *
from web_app import WebAPP
from imus_handler import ImusHandler

###############################################
sensors_id = ["88:6B:0F:E1:D8:68"]
###############################################

def thread_function(imus: ImusHandler):
    while True:
        imus.read_data()
        # print("thread_function:")
        # print(imus.imus_obj.values())
        time.sleep(0.0001)


#############################

class Server:
    def __init__(self, imus_in: ImusHandler):
        # global imus
        # imus = imus_in
        self.imus = imus_in
        self.ans = {}
        x = threading.Thread(target=thread_function, args=(self.imus,))
        x.start()

    def run(self):
        x = threading.Thread(target=thread_function, args=(self.imus,))
        x.start()

    def get_data(self):
        self.ans['ACC-X'] = list(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['ACC-X'])
        self.ans['ACC-Y'] = list(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['ACC-Y'])
        self.ans['ACC-Z'] = list(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['ACC-Z'])
        self.ans['GYRO-X'] = list(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['GYRO-X'])
        self.ans['GYRO-Y'] = list(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['GYRO-Y'])
        self.ans['GYRO-Z'] = list(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['GYRO-Z'])
        self.ans['Angle-X'] = list(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['Angle-X'])
        self.ans['Angle-Y'] = list(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['Angle-Y'])
        self.ans['Angle-Z'] = list(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['Angle-Z'])
        # print(type(self.ans[0]))
        #return np.array(self.ans)
        #return np.array(self.ans)
        #print(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['ACC-X'])
