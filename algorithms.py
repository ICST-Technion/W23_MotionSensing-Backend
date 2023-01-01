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

        # self.plot_options = ['ACC0-X', 'ACC0-Y', 'ACC0-Z', 'GYRO0-X', 'GYRO0-Y', 'GYRO0-Z']
        self.plot_options = {'ACC': ['ACC-X', 'ACC-Y', 'ACC-Z'], 'GYRO': ['GYRO-X', 'GYRO-Y', 'GYRO-Z'],
                             'Quat': ['Quat-0', 'Quat-1', 'Quat-2', 'Quat-3'], 'Euler Angles': ['Roll', 'Pitch', 'Yaw']}

        # for sensor_idx in range(len(imus.sensors_ids)):
        #     self.plot_options += [f"Yaw{sensor_idx}", f"Pitch{sensor_idx}", f"Roll{sensor_idx}",
        #                           f"Acc{sensor_idx}_X", f"Acc{sensor_idx}_Y", f"Acc{sensor_idx}_z",
        #                           f"Gyro{sensor_idx}_X", f"Gyro{sensor_idx}_Y", f"Gyro{sensor_idx}_z",
        #                           f"Quat{sensor_idx}_0", f"Quat{sensor_idx}_1", f"Quat{sensor_idx}_2",
        #                           f"Quat{sensor_idx}_3"
        #                           ]

        # for sensor_idx in range(len(imus.sensors_ids)):
        #     self.plot_options += [f"Yaw{sensor_idx}", f"Pitch{sensor_idx}", f"Roll{sensor_idx}",
        #                           f"Acc{sensor_idx}_X", f"Acc{sensor_idx}_Y", f"Acc{sensor_idx}_z",
        #                           f"Gyro{sensor_idx}_X", f"Gyro{sensor_idx}_Y", f"Gyro{sensor_idx}_z",
        #                           f"Quat{sensor_idx}_0", f"Quat{sensor_idx}_1", f"Quat{sensor_idx}_2",
        #                           f"Quat{sensor_idx}_3"
        #                           ]

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

                self.data[self.imus.sensors_ids[sensor_idx]] = {
                    f"Yaw": Yaw,
                    f"Pitch": Pitch,
                    f"Roll": Roll,
                    f"ACC-X": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-X']),
                    f"ACC-Y": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-Y']),
                    f"ACC-Z": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-Z']),
                    f"GYRO-X": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-X']),
                    f"GYRO-Y": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-Y']),
                    f"GYRO-Z": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-Z']),
                    f"Quat-0": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-0']),
                    f"Quat-1": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-1']),
                    f"Quat-2": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-2']),
                    f"Quat-3": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-3']),
                }
            else:
                self.data[self.imus.sensors_ids[sensor_idx]] = {
                    f"Yaw": 0,
                    f"Pitch": 0,
                    f"Roll": 0,
                    f"ACC-X": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-X']),
                    f"ACC-Y": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-Y']),
                    f"ACC-Z": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-Z']),
                    f"GYRO-X": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-X']),
                    f"GYRO-Y": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-Y']),
                    f"GYRO-Z": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-Z']),
                    f"Quat-0": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-0']),
                    f"Quat-1": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-1']),
                    f"Quat-2": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-2']),
                    f"Quat-3": list(
                        self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-3']),
                }

            # print(f'fb threshold: {self.settings["Feedback threshold"]}')
            # print(f'roll={self.data[f"Roll{sensor_idx}"]} pitch={self.data[f"Pitch{sensor_idx}"]} yaw={self.data[f"Yaw{sensor_idx}"]}')
            # print(self.data)

        return self.data

    def calc_euler_angles(self, data):
        return 1, 1, 1



