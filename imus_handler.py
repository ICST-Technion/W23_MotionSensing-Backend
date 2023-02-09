import threading
import numpy as np
from consts import DEBUG_MODE
from imu_object import ImuObject
from sage_motion_connection import SageMotionConnection

# Create a semaphore with a maximum count of 1
imu_object_semaphore = threading.Semaphore(1)

class ImusHandler(SageMotionConnection):
    def __init__(self):
        self.imus_obj = None
        self.imu_index_list = None
        self.can_start_data_reading = False
        SageMotionConnection.__init__(self)
        self.calculate_euler_angles = True
        self.pre_time = 0

        # f = open('config.json')
        # configurations = json.load(f)
        # sensors_ids = configurations['imu_ids']
        # feedback_array = configurations['feedback_ids']
        # SageMotionConnection.__init__(self, sensors_ids=sensors_ids, feedback_array=feedback_array)
        # self.calculate_euler_angles = True
        # self.imu_index_list = [f"IMU-{i}" for i in range(len(sensors_ids))]
        # self.imus_obj = {imu_name: ImuObject(name=imu_name, mac_address=sensors_ids[idx], index=idx) for idx, imu_name in enumerate(self.imu_index_list)}
        # self.pre_time = 0
        # f.close()

    def should_calc_euler_angles(self, should_calc):
        self.calculate_euler_angles = should_calc

    def setup_connection(self, sensors_ids=[], feedback_array=[]):
        self.can_start_data_reading = False
        if sensors_ids is not None:
            self.sensors_ids = sensors_ids
            self.imu_index_list = [f"IMU-{i}" for i in range(len(self.sensors_ids))]
            self.imus_obj = {imu_name: ImuObject(name=imu_name, mac_address=self.sensors_ids[idx], index=idx) for
                             idx, imu_name in enumerate(self.imu_index_list)}
        if feedback_array is not None:
            self.feedback_array = feedback_array

        connection_state = self.setup_connection_sage()
        self.can_start_data_reading = True

        return connection_state

    def read_data(self):
        raw_data = self.get_raw_data()
        if raw_data is not None:
            if not DEBUG_MODE:
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
                        imu_object_semaphore.acquire()
                        self.imus_obj[imu_name].push_data(acc, gyro, quat, self.calculate_euler_angles)
                        self.imus_obj[imu_name].pre_timeStep = timeStep
                        imu_object_semaphore.release()

            else:
                    i = 0
                    for imu_data in raw_data:
                        imu_index = i
                        i += 1
                        timeStep = imu_data['Sampletime']
                        imu_name = self.imu_index_list[imu_index]

                        if self.imus_obj[imu_name].pre_timeStep == timeStep:
                            continue

                        if timeStep == 20632:
                            aaa = 0
                        acc = np.array([imu_data['AccelX'], imu_data['AccelY'], imu_data['AccelZ']]).tolist()
                        gyro = np.array([imu_data['GyroX'], imu_data['GyroY'], imu_data['GyroZ']]).tolist()
                        quat = np.array(
                            [imu_data['Quat1'], imu_data['Quat2'], imu_data['Quat3'], imu_data['Quat4']]).tolist()
                        imu_object_semaphore.acquire()
                        self.imus_obj[imu_name].push_data(acc, gyro, quat, self.calculate_euler_angles)
                        self.imus_obj[imu_name].pre_timeStep = timeStep
                        imu_object_semaphore.release()



