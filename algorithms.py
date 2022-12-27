from imus_handler import ImusHandler

class RawDataAlg:
    def __init__(self, imus: ImusHandler):
        self.properties = [{"type": "CheckList", "param_name": "Calculate Euler angles", "default_value": 0, "values": ["yes", "no"]},
                           {"type": "TextBox", "param_name": "Feedback threshold", "default_value": 3}
                           ]
        self.settings = {
            "Calculate Euler angles": "yes",
            "Feedback threshold": 3
        }
        self.plot_options = []
        for sensor_idx in range(len(imus.sensors_ids)):
            self.plot_options += [f"Yaw{sensor_idx}", f"Pitch{sensor_idx}", f"Roll{sensor_idx}",
                                  f"Acc{sensor_idx}_X", f"Acc{sensor_idx}_Y", f"Acc{sensor_idx}_z",
                                  f"Gyro{sensor_idx}_X", f"Gyro{sensor_idx}_Y", f"Gyro{sensor_idx}_z",
                                  f"Quat{sensor_idx}_0", f"Quat{sensor_idx}_1", f"Quat{sensor_idx}_2",
                                  f"Quat{sensor_idx}_3"
                                  ]

        # self.sage = sage
        # self.settings = {}
        self.imus = imus
        self.data = {}
        self.name = 'raw_data'

    def set_properties(self, properties):
        self.properties = properties

    def run(self):
        # data = self.imus.read_data()
        for sensor_idx in range(len(self.imus.sensors_ids)):
            if self.settings["Calculate Euler angles"] == "yes":
                Yaw, Pitch, Roll = self.calc_euler_angles(self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data)

                self.data = {
                    f"Yaw{sensor_idx}": Yaw,
                    f"Pitch{sensor_idx}": Pitch,
                    f"Roll{sensor_idx}": Roll,
                    f"ACC{sensor_idx}-X": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-X']),
                    f"ACC{sensor_idx}-Y": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-Y']),
                    f"ACC{sensor_idx}-Z": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-Z']),
                    f"GYRO{sensor_idx}-X": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-X']),
                    f"GYRO{sensor_idx}-Y": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-Y']),
                    f"GYRO{sensor_idx}-Z": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-Z']),
                    f"Quat{sensor_idx}-0": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-0']),
                    f"Quat{sensor_idx}-1": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-1']),
                    f"Quat{sensor_idx}-2": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-2']),
                    f"Quat{sensor_idx}-3": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-3']),
                }
            else:
                self.data = {
                    f"Yaw{sensor_idx}": 0,
                    f"Pitch{sensor_idx}": 0,
                    f"Roll{sensor_idx}": 0,
                    f"ACC{sensor_idx}-X": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-X']),
                    f"ACC{sensor_idx}-Y": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-Y']),
                    f"ACC{sensor_idx}-Z": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-Z']),
                    f"GYRO{sensor_idx}-X": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-X']),
                    f"GYRO{sensor_idx}-Y": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-Y']),
                    f"GYRO{sensor_idx}-Z": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-Z']),
                    f"Quat{sensor_idx}-0": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-0']),
                    f"Quat{sensor_idx}-1": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-1']),
                    f"Quat{sensor_idx}-2": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-2']),
                    f"Quat{sensor_idx}-3": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-3']),
                }

            print(f'fb threshold: {self.settings["Feedback threshold"]}')
            print(f'roll={self.data[f"Roll{sensor_idx}"]} pitch={self.data[f"Pitch{sensor_idx}"]} yaw={self.data[f"Yaw{sensor_idx}"]}')

        return self.data

    def calc_euler_angles(self, data):
        return 1, 1, 1



