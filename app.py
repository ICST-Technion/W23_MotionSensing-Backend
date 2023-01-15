from flask import Flask, request, jsonify
from server import Server
from imus_handler import ImusHandler


app = Flask(__name__)

###############################################
# connect to sensors
imus = ImusHandler()
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
        elif request_type == 'get_imus':
            json_file['imus'] = server.get_imus()
        elif request_type == 'get_data_types':
            json_file['data_types'] = server.get_data_types()
        elif request_type == 'set_params':
            params = request.get_json()
            if params is not None:
                server.cur_alg.set_settings(params)
                # for key in params:
                #     server.cur_alg.settings[key] = params[key]

        return jsonify(json_file)


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080, threads=10)
    # app.run()
