from consts import *
from web_app import WebAPP
import pandas as pd
import requests  # websocket-client and requests libraries are required
import json
import websocket
from consts import *


class Vibration:
    def __init__(self, connection, sensor_id):
        self.connection = connection
        self.sensor_id = sensor_id

    def vibrate(self, duration):
        # Send a vibration command to the IMU sensor
        command = {"sensor_id": self.sensor_id, "duration": duration}
        self.connection.ws.send(json.dumps({"command": "vibrate", "data": command}))
