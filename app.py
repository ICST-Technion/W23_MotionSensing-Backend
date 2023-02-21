import datetime
import logging
import os
import threading
import time

from flask import Flask, request, jsonify
from waitress import serve

from consts import *
from imus_handler import ImusHandler
from server import Server

now = datetime.datetime.now()
log_file = str(now.date()) \
           + "--" \
           + str(now.time().hour) \
           + "-" \
           + str(now.time().minute) \
           + "-" \
           + str(now.time().second) \
           + "--backend.log"

formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')

handler = logging.FileHandler(log_file)
handler.setFormatter(formatter)

logging.basicConfig(
    # filename=log_file,
    # format=formatter.format(),
    level=logging.DEBUG,
    handlers=[
        handler
    ]
)

app = Flask(__name__)

last_request_time = time.time()
app_timeout = 30


def check_timeout(logger: logging.Logger):
    while True:
        if time.time() - last_request_time > app_timeout:  # check if 10 seconds have passed since the last request
            logger.info(f"No requests received for {app_timeout} seconds - exiting")
            if server.imus.ws is not None:  # close the websocket if it is open
                server.imus.ws.close()
                logger.info(f"Websocket closed")
            os.system('taskkill /f /t /pid %d' % os.getpid())  # terminate the app
        time.sleep(2)  # wait 10 seconds before checking again


###############################################
# connect to sensors
imus = ImusHandler()
server = Server(imus)


###############################################

@app.before_request
def before_request():
    global last_request_time
    last_request_time = time.time()


@app.route('/keepalive')
def keepalive_handler():
    app.logger.info(f"Got keepalive message from frontend")
    return '0'


@app.route('/stream')
def streamed_response():
    ans = server.alg_run()
    ans['feedback_active'] = 'Yes' if server.imus.feedback_activated else 'No'
    return jsonify(ans)


@app.route('/', methods=['GET', 'POST'])
def server_run():
    args = request.args
    json_file = {}
    request_type = args.get('request_type', type=str)
    app.logger.info(f"Got request {request_type} from app")
    if request_type == 'algorithms':
        json_file[request_type] = server.get_algorithm_list()
    elif request_type == 'set_cur_alg':
        alg = request.get_json()
        if alg in server.algorithms:
            server.set_cur_alg(alg)
        else:
            app.logger.error(f"Got a non existing algorithm name: {alg} from app")
            app.logger.error(f"Bad alg name: {alg}")
        return alg
    elif request_type == 'get_params':
        json_file['params'] = server.get_alg_properties()
    elif request_type == 'get_batteries':
        json_file['batteries'] = server.imus.get_imu_batteries()
    elif request_type == 'get_imus':
        json_file['imus'] = server.get_imus()
    elif request_type == 'get_data_types':
        json_file['data_types'] = server.get_data_types()
    elif request_type == 'get_cur_alg':
        json_file['cur_alg'] = server.get_cur_alg()
    elif request_type == 'set_params':
        params = request.get_json()
        if params is not None:
            server.cur_alg.set_settings(params)
    elif request_type == 'set_imus':
        imus = request.get_json()
        if imus is not None:
            connection_state = server.restart_server(sensors_ids=imus['imus'], feedback_array=imus['feedbacks'])
            app.logger.info(f'Connected to imus: {server.imus.sensors_ids}\nfeedbacks: {server.imus.feedback_array}')
            # server.imus.can_start = True
            json_file['connection_state'] = connection_state
    app.logger.info(f"Sending answer for request {request_type} to app")
    return jsonify(json_file)


if __name__ == '__main__':
    t = threading.Thread(target=check_timeout, args=(app.logger,))
    t.start()
    serve(app, host='0.0.0.0', port=PORT, threads=10)
    # app.run(debug=True)
