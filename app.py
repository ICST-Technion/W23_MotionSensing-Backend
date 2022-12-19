from flask import Flask, request, jsonify
from server import Server
from imus_handler import ImusHandler
import os

app = Flask(__name__)

###############################################
sensors_id = ["88:6B:0F:E1:D8:68"]
###############################################
# connect to sensors
imus = ImusHandler(sensors_id)
###############################################
server = Server(imus)


###############################################

def get_algorithm_list():
    algorithms = []
    for name in os.listdir('algorithms'):
        path = 'algorithms/' + name
        if os.path.isdir(path):
            algorithms.append(name)

    return algorithms


'''
arg keys:
"raw_data"
TODO: add algorithm arguments 
and run the corresponding algorithm script + return results
'''

requests = {'algorithms', 'raw_data'}


@app.route('/', methods=['GET'])
def server_run():  # put application's code here
    args = request.args
    while True:
        json_file = {}
        request_type = args.get('request_type', type=str)
        if request_type == 'algorithms':
            json_file[request_type] = get_algorithm_list()

        elif request_type == 'raw_data':
            server.get_data()
            json_file['ACC-X'] = server.ans['ACC-X']
            json_file['ACC-Y'] = server.ans['ACC-Y']
            json_file['ACC-Z'] = server.ans['ACC-Z']

            json_file['GYRO-X'] = server.ans['GYRO-X']
            json_file['GYRO-Y'] = server.ans['GYRO-Y']
            json_file['GYRO-Z'] = server.ans['GYRO-Z']

            json_file['Angle-X'] = server.ans['Angle-X']
            json_file['Angle-Y'] = server.ans['Angle-Y']
            json_file['Angle-Z'] = server.ans['Angle-Z']
        # else:
        #     json_file['data'] = 'Bad arg!'
        return jsonify(json_file)

        # arg = float(request.args['query'])
        # json_file = {}
        # if arg is not None:
        #     json_file['query'] = str(log10(arg))
        # else:
        #     json_file['query'] = 'Bad arg!'
        # return jsonify(json_file)


if __name__ == '__main__':
    # server.run()
    app.run()
    # web_app = WebAPP(imus)
    # web_app.run_app()
