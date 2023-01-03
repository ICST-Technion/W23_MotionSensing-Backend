from base_algorithm_class import Alg
from imus_handler import ImusHandler


class RawDataAlg(Alg):
    def __init__(self, imus: ImusHandler):
        Alg.__init__(
            self,
            properties=[
                {"type": "CheckList", "param_name": "Calculate Euler angles", "default_value": 0,
                 "values": ["yes", "no"]},
                {"type": "TextBox", "param_name": "Feedback threshold", "default_value": 3}
            ],
            settings={
                "Calculate Euler angles": "yes",
                "Feedback threshold": 3
            },
            plot_options={'ACC': ['ACC-X', 'ACC-Y', 'ACC-Z'], 'GYRO': ['GYRO-X', 'GYRO-Y', 'GYRO-Z'],
                          'Quat': ['Quat-0', 'Quat-1', 'Quat-2', 'Quat-3'], 'Euler Angles': ['Roll', 'Pitch', 'Yaw']},
            imus=imus,
            name='raw_data'
        )

        # self.plot_options = ['ACC0-X', 'ACC0-Y', 'ACC0-Z', 'GYRO0-X', 'GYRO0-Y', 'GYRO0-Z']

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
        self.data = {}

    def set_settings(self, settings):
        if settings is not None:
            for key in settings:
                self.settings[key] = settings[key]
        if self.settings['Calculate Euler angles'] == 'yes':
            self.imus.should_calc_euler_angles(True)
        else:
            self.imus.should_calc_euler_angles(False)

    def quant2rotation_andEulerAngles(self, qw, qx, qy, qz, degrees_flag=True):
        # X_G = R_GS * X_s
        # M = R_GS
        # R_GS = R_SG ^ T
        # R_GS = Rz(ψ) * Ry(θ) * Rx(φ)

        # norm
        q_norm = np.linalg.norm(np.array([qw, qx, qy, qz]))
        qw /= q_norm
        qx /= q_norm
        qy /= q_norm
        qz /= q_norm

        qww = qw * qw
        qwx = qw * qx
        qwy = qw * qy
        qwz = qw * qz
        qxx = qx * qx
        qxy = qx * qy
        qxz = qx * qz
        qyy = qy * qy
        qyz = qy * qz
        qzz = qz * qz
        #
        roll_x = np.arctan2((2 * qyz + 2 * qwx),
                            (1 - 2 * (qxx + qyy)))  # φ = roll = rotation around XG, defined from [-180°…180°]
        pitch_y = np.arcsin(2 * qwy - 2 * qxz)  # θ = pitch = rotation around YG, defined from [-90°…90°]
        yaw_z = np.arctan2((2 * qxy + 2 * qwz),
                           (1 - 2 * (qyy + qzz)))  # ψ = yaw = rotation around ZG, defined from [-180°…180°]

        # Rotation matrix from EulerAngles
        R_GS = Rz(yaw_z) * Ry(pitch_y) * Rx(roll_x)
        # Rotation matrix from quaternions
        M_GS = 2 * np.array([[qww + qxx - 0.5, qxy - qwz, qxz + qwy],
                             [qxy + qwz, qww + qyy - 0.5, qyz - qwx],
                             [qxz - qwy, qyz + qwx, qww + qzz - 0.5]])

        # R_GS should be equal to M_GS

        # Convert to degrees
        if degrees_flag:
            roll_x = roll_x * (180 / np.pi)
            pitch_y = pitch_y * (180 / np.pi)
            yaw_z = yaw_z * (180 / np.pi)

        return M_GS, roll_x, pitch_y, yaw_z

    def run(self):
        # data = self.imus.read_data()
        for sensor_idx in range(len(self.imus.sensors_ids)):
            # if self.settings["Calculate Euler angles"] == "yes":
            # Yaw, Pitch, Roll = self.calc_euler_angles(self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data)

            self.data[self.imus.sensors_ids[sensor_idx]] = {
                f"Yaw": list(
                    self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Yaw']),
                f"Pitch": list(
                    self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Pitch']),
                f"Roll": list(
                    self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Roll']),
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
            # else:
            #     self.data[self.imus.sensors_ids[sensor_idx]] = {
            #         f"Yaw": 0,
            #         f"Pitch": 0,
            #         f"Roll": 0,
            #         f"ACC-X": list(
            #             self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-X']),
            #         f"ACC-Y": list(
            #             self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-Y']),
            #         f"ACC-Z": list(
            #             self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['ACC-Z']),
            #         f"GYRO-X": list(
            #             self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-X']),
            #         f"GYRO-Y": list(
            #             self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-Y']),
            #         f"GYRO-Z": list(
            #             self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['GYRO-Z']),
            #         f"Quat-0": list(
            #             self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-0']),
            #         f"Quat-1": list(
            #             self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-1']),
            #         f"Quat-2": list(
            #             self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-2']),
            #         f"Quat-3": list(
            #             self.imus.imus_obj[self.imus.imu_index_list[sensor_idx]].imu_data['Quat-3']),
            #     }
            #
            # print(f'fb threshold: {self.settings["Feedback threshold"]}')
            # print(f'roll={self.data[f"Roll{sensor_idx}"]} pitch={self.data[f"Pitch{sensor_idx}"]} yaw={self.data[f"Yaw{sensor_idx}"]}')
            # for imu in self.imus.sensors_ids:
            #     print(f'id: {imu} accx: {self.data[imu]["ACC-X"]}')
            # print(self.imus.sensors_ids)

        return self.data

    def calc_euler_angles(self, data):
        return 1, 1, 1
