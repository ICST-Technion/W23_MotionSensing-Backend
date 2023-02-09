import copy
import logging
import os
import threading

import numpy as np
import pandas as pd
import websocket
import websockets
import requests  # websocket-client and requests libraries are required
import json
from consts import *
import unittest.mock as mock

app_logger = logging.getLogger(__name__)

# Create a semaphore with a maximum count of 1
semaphore = threading.Semaphore(1)

class SageMotionConnection:
    def __init__(self):
        self.web_url = None
        self.stream_thread = None
        self.debug_data_df = None
        self.data_row_counter = None
        self.ws = None
        self.feedback_array = None
        self.sensors_ids = None
        self.raw_data = None

    def on_message(self, wsapp, message):
        semaphore.acquire()
        self.raw_data = message
        semaphore.release()

    @staticmethod
    def on_ping(wsapp, message):
        app_logger.info("Got a ping! A pong reply has already been automatically sent.")

    @staticmethod
    def on_pong(wsapp, message):
        app_logger.info("Got a pong! No need to respond")

    @staticmethod
    def on_error(wsapp, message):
        app_logger.error(message)

    def setup_connection_sage(self):
        # print('setting up connection')
        connection_status = {}
        hub_addr = "192.168.137.1"  # fixed address for wired connect with SageHub
        self.web_url = "http://" + hub_addr + "/api/v1/"
        request_json = {"sensor_pairings": self.sensors_ids,
                        "feedback_pairings": self.feedback_array}
        request_params = {"version_id": "510e53970c"}

        if not DEBUG_MODE:
            app_logger.info(f"Setting up sage connection")
            # pair nodes
            print("Connecting to nodes...")
            r = requests.put(self.web_url + 'nodes/connected', json=request_json, params=request_params)
            # connection_status = r.text
            print(connection_status)
            # start data collection
            r = requests.post(self.web_url + 'enabled_apps/current', params={"command": "start"})
            print(r.text)
            r = requests.get(self.web_url + 'system_status')
            system_status = r.json()
            connection_status['imus'] = []
            connection_status['feedbacks'] = []
            if system_status is not None:
                for sensor_data in system_status['sage_status']['sensor']:
                    connection_status['imus'].append(sensor_data['hwAddress'])
                for sensor_data in system_status['sage_status']['feedback']:
                    connection_status['feedbacks'].append(sensor_data['hwAddress'])
            # self.ws = websocket.create_connection("ws://" + hub_addr + ":5678")
        else:
            app_logger.info(f"Setting up debug mode sage connection")
            connection_status['imus'] = self.sensors_ids
            connection_status['feedbacks'] = self.feedback_array
            hub_addr = "localhost"

        if self.ws is not None:
            app_logger.info(f"Closing socket")
            self.ws.close()
        connection_status = {'imus': self.sensors_ids, 'feedbacks': self.feedback_array}
        # websocket.setdefaulttimeout(None)
        app_logger.info(f"Opening a new socket with url: " + "ws://" + f"{hub_addr}" + ":5678")
        self.ws = websocket.WebSocketApp("ws://" + hub_addr + ":5678",
                                         on_ping=self.on_ping,
                                         on_message=self.on_message,
                                         on_pong=self.on_pong)
        self.stream_thread = threading.Thread(target=lambda: self.ws.run_forever(ping_interval=45, ping_timeout=30))
        self.stream_thread.start()
        return connection_status

    def get_imu_batteries(self):
        r = requests.get(self.web_url + 'system_status').json()
        batteries = {}
        for sensor_stats in r['sage_status']['sensor']:
            batteries[sensor_stats['hwAddress']] = sensor_stats['battery']
        for sensor_stats in r['sage_status']['feedback']:
            batteries[sensor_stats['hwAddress']] = sensor_stats['battery']
        return batteries

    def get_raw_data(self):
        semaphore.acquire()
        if self.raw_data == '' or self.raw_data is None:
            semaphore.release()
            return
        if not DEBUG_MODE:
            raw_data = json.loads(self.raw_data)["raw_data"]
            semaphore.release()
            return raw_data

        raw_data = json.loads(self.raw_data)["raw_data"]
        semaphore.release()
        data = [copy.deepcopy(raw_data[0]) for imu_index in range(len(self.sensors_ids))]
        for i in range(len(data)):
            data[i]['AccelX'] *= (i+1)
            data[i]['AccelY'] *= (i + 1)
            data[i]['AccelZ'] *= (i + 1)
            data[i]['SensorIndex'] = i
            # print(data[i])
        # print(data)
        return data
