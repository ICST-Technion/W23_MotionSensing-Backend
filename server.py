import logging
import threading
import time
from imus_handler import ImusHandler
import algorithms

event = threading.Event()
app_logger = logging.getLogger(__name__)

def thread_function(imus: ImusHandler):
    while True:
        if event.isSet():
            break
        imus.read_data()
        # print("thread_function:")
        # print(imus.imus_obj.values())
        time.sleep(0.01)


#############################

class Server:
    def __init__(self, imus_in: ImusHandler):
        # global imus
        # imus = imus_in
        self.imus = imus_in
        # self.ans = {}
        self.algorithms = {
            'Raw Data': algorithms.RawDataAlg(self.imus)
        }
        self.cur_alg = list(self.algorithms.values())[0]
        # self.data_read_thread = threading.Thread(target=thread_function, args=(self.imus,))
        # self.data_read_thread.start()
        self.data_read_thread = None
        self.alg_output = None

    def restart_server(self, sensors_ids=[], feedback_array=[]):
        app_logger.info(f"Restarting hub connection")
        if self.data_read_thread is not None:
            event.set()
            self.data_read_thread.join()
            event.clear()
        self.imus.can_start_data_reading = True
        # if self.imus.sensors_ids:
        #     connection_state = self.imus.setup_connection(sensors_ids=self.imus.sensors_ids, feedback_array=self.imus.feedback_array)
        # else:
        connection_state = self.imus.setup_connection(sensors_ids=sensors_ids,
                                                      feedback_array=feedback_array)
        self.data_read_thread = threading.Thread(target=thread_function, args=(self.imus,))
        self.data_read_thread.start()
        app_logger.info(f"Started a new data reading thread from hub")
        return connection_state

    def get_cur_alg(self):
        return self.cur_alg.name

    def set_cur_alg(self, alg):
        app_logger.info(f"Setting current algorithm to {alg}")
        self.cur_alg = self.algorithms[alg]

    def get_alg_properties(self):
        app_logger.info(f"Getting algorithm properties")
        return self.cur_alg.properties

    def get_imus(self):
        return self.imus.sensors_ids

    def set_alg_properties(self, properties):
        app_logger.info(f"Setting algorithm properties")
        self.cur_alg.set_properties(properties)

    def get_algorithm_list(self):
        app_logger.info(f"Getting algorithms list")
        return list(self.algorithms.keys())

    def get_data_types(self):
        app_logger.info(f"Getting get data types")
        return self.cur_alg.plot_options

    def run(self):
        x = threading.Thread(target=thread_function, args=(self.imus,))
        x.start()

    def alg_run(self):
        return self.cur_alg.run()

        # print(type(self.ans[0]))
        # return np.array(self.ans)
        # return np.array(self.ans)
        # print(self.imus.imus_obj[self.imus.imu_index_list[0]].imu_data['ACC-X'])
