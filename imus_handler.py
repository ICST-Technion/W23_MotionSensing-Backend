import numpy as np
from imu_object import ImuObject
from sage_motion_connection import SageMotionConnection

N = 1000


class ImusHandler(SageMotionConnection):
    def __init__(self, sensors_ids=("88:6B:0F:E1:D8:98"), feedback_array=()):
        SageMotionConnection.__init__(self, sensors_ids=sensors_ids, feedback_array=feedback_array)

        self.imu_index_list = [f"IMU-{i}" for i in range(len(sensors_ids))]
        self.imus_obj = {imu_name: ImuObject(name=imu_name, mac_address=sensors_ids[idx], index=idx) for idx, imu_name in enumerate(self.imu_index_list)}
        self.pre_time = 0

    def read_data(self):
        raw_data = self.get_raw_data()

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

