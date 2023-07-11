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

        # file_path = 'C:\\Users\\odztm\\PycharmProjects\\Alon_code_for_IOT\\imus_raw_data_GUI\\abc.csv'
        # header = ['ACC-X', 'ACC-Y', 'ACC-Z', 'Quat-W', 'Quat-X', 'Quat-Y', 'Quat-Z']
        # file2save = open(file_path, 'w', newline='')
        # self.csv_writer = csv.writer(file2save)
        # self.csv_writer.writerow(header)

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


    # def save_to_csv(self, data):
    #     for row in data:
    #         self.csv_writer.writerow(row)

    def push_data(self, acc, gyro, quat, calc_euler_angles):
        roll, pitch, yaw = 0, 0, 0

        # if calc_euler_angles:
        #     M, roll, pitch, yaw = self.quant2rotation_andEulerAngles(quat[0], quat[1], quat[2], quat[3],
        #                                                              degrees_flag=True)
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

        # self.imu_data['Roll'].append(roll)
        # self.imu_data['Pitch'].append(pitch)
        # self.imu_data['Yaw'].append(yaw)

        # self.save_to_csv([[acc[0], acc[1], acc[2], quat[0], quat[1], quat[2], quat[3]]])
