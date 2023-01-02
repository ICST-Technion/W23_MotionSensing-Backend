import numpy as np
import pandas as pd
import websocket
import requests  # websocket-client and requests libraries are required
import json
from consts import *

class SageMotionConnection:
    def __init__(self, sensors_ids=(), feedback_array=()):
        self.sensors_ids = sensors_ids
        self.feedback_array = feedback_array

        hub_addr = "192.168.137.1"  # fixed address for wired connect with SageHub
        web_url = "http://" + hub_addr + "/api/v1/"

        # request_json = {"sensor_pairings": sensors_ids, "feedback_pairings": feedback_array}
        request_json = {"sensor_pairings": ["88:6B:0F:E1:D8:48"],
                        "feedback_pairings": []}
        request_params = {"version_id": "510e53970c"}

        if not DEBUG_MODE:
            # pair nodes
            print("Connecting to nodes...")
            r = requests.put(web_url + 'nodes/connected', json=request_json, params=request_params)
            print(r.text)
            # start data collection
            r = requests.post(web_url + 'enabled_apps/current', params={"command": "start"})
            print(r.text)

            self.ws = websocket.create_connection("ws://" + hub_addr + ":5678")
        else:
            print('Debug mode connection')
            self.data_row_counter = 0
            self.debug_data_df = pd.read_csv('debug_mode_data.csv')  # one IMU data placed on the lab origin axis
            self.debug_data_df.columns = [self.debug_data_df.columns[i].replace('_1', '') for i in range(self.debug_data_df.columns.shape[0])]

    def get_com_message(self):
        message = self.ws.recv()
        return message

    def get_raw_data(self):
        raw_data = {}
        if not DEBUG_MODE:
            message = self.get_com_message()
            if message == '':
                return
            raw_data = json.loads(message)["raw_data"]
            # print(raw_data)
        else:
            data_row = self.debug_data_df.iloc[self.data_row_counter]
            if self.data_row_counter == self.debug_data_df.shape[0]-1:
                self.data_row_counter = 0
            else:
                self.data_row_counter += 1
            raw_data = [data_row for i in self.sensors_ids]  # create dummy data for each IMU
        return raw_data
