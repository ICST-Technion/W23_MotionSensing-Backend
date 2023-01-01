import numpy as np
import collections
import pandas as pd
import threading
import time
from consts import *
from web_app import WebAPP
from imus_handler import ImusHandler
import algorithms


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
        # self.ans = {}
        self.algorithms = {
            'raw_data': algorithms.RawDataAlg(self.imus)
        }
        self.cur_alg = self.algorithms['raw_data']
        x = threading.Thread(target=thread_function, args=(self.imus,))
        x.start()

    def set_cur_alg(self, alg):
        self.cur_alg = self.algorithms[alg]

    def get_alg_properties(self):
        return self.cur_alg.properties

    def get_imus(self):
        return self.imus.sensors_ids

    def set_alg_properties(self, properties):
        self.cur_alg.properties = properties

    def get_algorithm_list(self):
        return list(self.algorithms.keys())

    def get_data_types(self):
        return self.cur_alg.plot_options

    def run(self):
        x = threading.Thread(target=thread_function, args=(self.imus,))
        x.start()

    def alg_run(self):
        return self.cur_alg.run()

        # print(type(self.ans[0]))
        # return np.array(self.ans)
        # return np.array(self.ans)
        # print(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['ACC-X'])
