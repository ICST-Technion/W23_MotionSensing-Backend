import numpy as np
import collections
import plotly.express as px
import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

#####################################################
Rz = lambda a: np.array([[np.cos(a), -np.sin(a), 0],
                         [np.sin(a),  np.cos(a), 0],
                         [   0,          0,      1]])

Ry = lambda a: np.array([[ np.cos(a), 0, np.sin(a)],
                         [    0,      1,    0     ],
                         [-np.sin(a), 0, np.cos(a)]])

Rx = lambda a: np.array([[1,    0,          0     ],
                         [0, np.cos(a), -np.sin(a)],
                         [0, np.sin(a),  np.cos(a)]])
#####################################################
tt_debug = 0
fig = plt.figure()

class ImuObject:
    def __init__(self, name, mac_address, index):
        self.name = name
        self.mac_address = mac_address
        self.index = index
        self.color = px.colors.qualitative.Plotly[index]
        self.imu_data = {}
        self.pre_timeStep = 0
        self.enabled = True
        self.used_as_feedback = False

        file_path = 'C:\\Users\\odztm\\PycharmProjects\\Alon_code_for_IOT\\imus_raw_data_GUI\\abc.csv'
        header = ['ACC-X', 'ACC-Y', 'ACC-Z', 'Quat-W', 'Quat-X', 'Quat-Y', 'Quat-Z']
        file2save = open(file_path, 'w', newline='')
        self.csv_writer = csv.writer(file2save)
        self.csv_writer.writerow(header)

        #
        N = 1

        self.imu_data = {
            'Roll': collections.deque(maxlen=N),
            'Pitch': collections.deque(maxlen=N),
            'Yaw': collections.deque(maxlen=N)
        }
        for imu_data_type in ['ACC', 'GYRO', 'Angle', 'Quat']:
            if imu_data_type == 'Quat':
                for i in range(4):
                    self.imu_data[f'{imu_data_type}-{i}'] = collections.deque(maxlen=N)
            else:
                for axis in ['X', 'Y', 'Z']:
                    self.imu_data[f'{imu_data_type}-{axis}'] = collections.deque(maxlen=N)


    def save_to_csv(self, data):
        for row in data:
            self.csv_writer.writerow(row)

    def push_data(self, acc, gyro, quat, calc_euler_angles):
        roll, pitch, yaw = 0, 0, 0

        if calc_euler_angles:
            M, roll, pitch, yaw = self.quant2rotation_andEulerAngles(quat[0], quat[1], quat[2], quat[3],
                                                                     degrees_flag=True)
        # R_LG = np.array([[-0.7275223679275690,  0.68587613917894000, 0.01688567055386180],
        #                  [- 0.685932802495416, -0.72765835991016600, 0.00308248497683352],
        #                  [0.01440120223619500, -0.00933985855557795, 0.99985267535588200]])

        # acc = R_LG@(M@acc)
        # global tt_debug
        # tt_debug = tt_debug + 1
        # acc[0] = np.sin(2*np.pi*5*(tt_debug/100))

        # acc[0] += - 1
        # acc[1] += 10
        # acc[2] += + 2

        self.imu_data['ACC-X'].append(acc[0])
        self.imu_data['ACC-Y'].append(acc[1])
        self.imu_data['ACC-Z'].append(acc[2])

        self.imu_data['GYRO-X'].append(gyro[0])
        self.imu_data['GYRO-Y'].append(gyro[1])
        self.imu_data['GYRO-Z'].append(gyro[2])

        self.imu_data['Quat-0'].append(quat[0])
        self.imu_data['Quat-1'].append(quat[1])
        self.imu_data['Quat-2'].append(quat[2])
        self.imu_data['Quat-3'].append(quat[3])

        self.imu_data['Roll'].append(roll)
        self.imu_data['Pitch'].append(pitch)
        self.imu_data['Yaw'].append(yaw)

        self.save_to_csv([[acc[0], acc[1], acc[2], quat[0], quat[1], quat[2], quat[3]]])

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
        roll_x = np.arctan2((2 * qyz + 2 * qwx), (1 - 2 * (qxx + qyy)))  # φ = roll = rotation around XG, defined from [-180°…180°]
        pitch_y = np.arcsin(2 * qwy - 2 * qxz)                           # θ = pitch = rotation around YG, defined from [-90°…90°]
        yaw_z = np.arctan2((2 * qxy + 2 * qwz), (1 - 2 * (qyy + qzz)))   # ψ = yaw = rotation around ZG, defined from [-180°…180°]

        # Rotation matrix from EulerAngles
        R_GS = Rz(yaw_z) * Ry(pitch_y) * Rx(roll_x)
        # Rotation matrix from quaternions
        M_GS = 2 * np.array([[qww + qxx - 0.5, qxy - qwz      , qxz + qwy],
                             [qxy + qwz      , qww + qyy - 0.5, qyz - qwx],
                             [qxz - qwy      , qyz + qwx      , qww + qzz - 0.5]])

        # R_GS should be equal to M_GS

        # Convert to degrees
        if degrees_flag:
            roll_x = roll_x * (180 / np.pi)
            pitch_y = pitch_y * (180 / np.pi)
            yaw_z = yaw_z * (180 / np.pi)

        return M_GS, roll_x, pitch_y, yaw_z