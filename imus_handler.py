import numpy as np
from imu_object import ImuObject
from sage_motion_connection import SageMotionConnection
import json
from consts import *

N = 1000


class ImusHandler(SageMotionConnection):
    def __init__(self):
        f = open('config.json')
        configurations = json.load(f)
        sensors_ids = configurations['imu_ids']
        feedback_array = configurations['feedback_ids']
        SageMotionConnection.__init__(self, sensors_ids=sensors_ids, feedback_array=feedback_array)
        self.calculate_euler_angles = True
        self.imu_index_list = [f"IMU-{i}" for i in range(len(sensors_ids))]
        self.imus_obj = {imu_name: ImuObject(name=imu_name, mac_address=sensors_ids[idx], index=idx) for idx, imu_name in enumerate(self.imu_index_list)}
        self.pre_time = 0
        f.close()

    def should_calc_euler_angles(self, should_calc):
        self.calculate_euler_angles = should_calc

    def read_data(self):
        raw_data = self.get_raw_data()
        if not DEBUG_MODE:
            if type(raw_data) is not None:
                for imu_data in raw_data:
                    imu_index = int(imu_data['SensorIndex'])
                    timeStep = imu_data['Sampletime']
                    imu_name = self.imu_index_list[imu_index]

                    if self.imus_obj[imu_name].pre_timeStep == timeStep:
                        continue

                    if timeStep == 20632:
                        aaa = 0

                    acc = np.array([imu_data['AccelX'], imu_data['AccelY'], imu_data['AccelZ']]).tolist()
                    gyro = np.array([imu_data['GyroX'], imu_data['GyroY'], imu_data['GyroZ']]).tolist()
                    quat = np.array([imu_data['Quat1'], imu_data['Quat2'], imu_data['Quat3'], imu_data['Quat4']]).tolist()

                    self.imus_obj[imu_name].push_data(acc, gyro, quat)
                    self.imus_obj[imu_name].pre_timeStep = timeStep

        else:
            for imu_index in range(len(self.sensors_ids)):
                if type(raw_data) is not None:
                    for imu_data in raw_data:
                        timeStep = imu_data['Sampletime']
                        imu_name = self.imu_index_list[imu_index]

                        if self.imus_obj[imu_name].pre_timeStep == timeStep:
                            continue

                        if timeStep == 20632:
                            aaa = 0

                        acc = np.array([imu_data['AccelX'], imu_data['AccelY'], imu_data['AccelZ']]).tolist()
                        for i in range(len(acc)):
                                acc[i] += 30 * imu_index

                        gyro = np.array([imu_data['GyroX'], imu_data['GyroY'], imu_data['GyroZ']]).tolist()
                        for i in range(len(gyro)):
                                gyro[i] += 30 * imu_index

                        quat = np.array(
                            [imu_data['Quat1'], imu_data['Quat2'], imu_data['Quat3'], imu_data['Quat4']]).tolist()

                        self.imus_obj[imu_name].push_data(acc, gyro, quat, self.calculate_euler_angles)
                        self.imus_obj[imu_name].pre_timeStep = timeStep

