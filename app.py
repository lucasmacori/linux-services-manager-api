from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify
from flask_cors import CORS
from pony.orm import *
from config import config
import services, json, auth

# Connexion à la base de données
if config['debug']:
    set_sql_debug(True)

# Création de l'application web
app = Flask(__name__)

# Configuration de CORS
CORS(app)

# Définition des routes de l'API
@app.route('/api/v1/login', methods=['POST'])
def login():
    return auth.login(request.data)

@app.route('/api/v1/services', methods=['GET'])
def get_service():
    logged_in, response, status_code = auth.check_token(request.headers.get('username'), request.headers.get('token'))
    if logged_in:
        return services.search_services()
    else:
        return response, status_code 

@app.route('/api/v1/services/<name>', methods=['GET'])
def get_specific_service(name):
    logged_in, response, status_code = auth.check_token(request.headers.get('username'), request.headers.get('token'))
    if logged_in:
        return services.search_services(name)
    else:
        return response, status_code 

@app.route('/api/v1/favorite/services', methods=['GET'])
def get_favorite_service():
    logged_in, response, status_code = auth.check_token(request.headers.get('username'), request.headers.get('token'))
    if logged_in:
        return services.search_favorite_services()
    else:
        return response, status_code

@app.route('/api/v1/favorite/services/<name>', methods=['GET'])
def get_specific_favorite_service(name):
    logged_in, response, status_code = auth.check_token(request.headers.get('username'), request.headers.get('token'))
    if logged_in:
        return services.search_favorite_services(name)
    else:
        return response, status_code

@app.route('/api/v1/favorite/services', methods=['POST'])
def create_favorite_service():
    logged_in, response, status_code = auth.check_token(request.headers.get('username'), request.headers.get('token'))
    if logged_in:
        return services.create_favorite_service(request.data)
    else:
        return response, status_code

@app.route('/api/v1/favorite/services/<name>', methods=['PUT'])
def edit_favorite_service(name):
    logged_in, response, status_code = auth.check_token(request.headers.get('username'), request.headers.get('token'))
    if logged_in:
        return services.edit_favorite_service(name, request.data)
    else:
        return response, status_code

@app.route('/api/v1/favorite/services/<name>', methods=['DELETE'])
def delete_favorite_service(name):
    logged_in, response, status_code = auth.check_token(request.headers.get('username'), request.headers.get('token'))
    if logged_in:
        return services.delete_favorite_service(name)
    else:
        return response, status_code

@app.route('/api/v1/service/<name>', methods=['PUT'])
def start_service(name):
    logged_in, response, status_code = auth.check_token(request.headers.get('username'), request.headers.get('token'))
    if logged_in:
        return services.start_service(name)
    else:
        return response, status_code
    
@app.route('/api/v1/service/<name>', methods=['DELETE'])
def stop_service(name):
    logged_in, response, status_code = auth.check_token(request.headers.get('username'), request.headers.get('token'))
    if logged_in:
        return services.stop_service(name)
    else:
        return response, status_code

# Démarrage de l'API
if __name__ == '__main__':
    if config['debug']:
        app.run(host='127.0.0.1', port=int(config['port']))
    else:
        if config['ssl'] and 'cert' in config and 'key' in config:
            http_server = WSGIServer(('', int(config['port'])), app, certfile = config['cert'], keyfile = config['key'])
        else:
            http_server = WSGIServer(('', int(config['port'])), app)
        http_server.serve_forever()