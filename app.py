from flask import Flask, request, jsonify
from server import Server
from imus_handler import ImusHandler


app = Flask(__name__)

###############################################
sensors_ids = ["88:6B:0F:E1:D8:68"]
###############################################

# connect to sensors
imus = ImusHandler(sensors_ids)
###############################################
server = Server(imus)


###############################################

'''
arg keys:
"raw_data"
TODO: add algorithm arguments 
and run the corresponding algorithm script + return results
'''

# @app.route('/set_params', methods=['POST'])
# def server_run2():
#     params = request.get_json()
#     if params is not None:
#         for key in params:
#             server.cur_alg.settings[key] = params[key]
#
#     return params

@app.route('/', methods=['GET', 'POST'])
def server_run():
    args = request.args
    while True:
        json_file = {}
        request_type = args.get('request_type', type=str)
        if request_type == 'algorithms':
            json_file[request_type] = server.get_algorithm_list()
        # elif request_type == 'set_alg_params': TODO
        elif request_type in server.algorithms:
            if request_type != server.cur_alg.name:
                server.set_cur_alg(request_type)
            json_file = server.alg_run()
        elif request_type == 'get_params':
            json_file['params'] = server.get_alg_properties()
        elif request_type == 'set_params':
            params = request.get_json()
            if params is not None:
                for key in params:
                    server.cur_alg.settings[key] = params[key]

        return jsonify(json_file)


if __name__ == '__main__':
    app.run()
