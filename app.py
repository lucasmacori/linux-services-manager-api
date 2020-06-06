from gevent.pywsgi import WSGIServer
from flask import Flask, request
from pony.orm import *
from config import config
import services, json

# Connexion à la base de données
if config['debug']:
    set_sql_debug(True)

# Création de l'application web
app = Flask(__name__)

# Définition des routes de l'API
@app.route('/api/v1/services', methods=['GET'])
def get_service():
    return services.search_services()

@app.route('/api/v1/services/<name>', methods=['GET'])
def get_specific_service(name):
    return services.search_services(name)

@app.route('/api/v1/favorite/services', methods=['GET'])
def get_favorite_service():
    return services.search_favorite_services()

@app.route('/api/v1/favorite/services/<name>', methods=['GET'])
def get_specific_favorite_service(name):
    return services.search_favorite_services(name)

@app.route('/api/v1/favorite/services', methods=['POST'])
def create_favorite_service():
    return services.create_favorite_service(request.data)

@app.route('/api/v1/favorite/services/<name>', methods=['PUT'])
def edit_favorite_service(name):
    return services.edit_favorite_service(name, request.data)

@app.route('/api/v1/favorite/services/<name>', methods=['DELETE'])
def delete_favorite_service(name):
    return services.delete_favorite_service(name)

@app.route('/api/v1/service/<name>', methods=['PUT'])
def start_service(name):
    return services.start_service(name)
    
@app.route('/api/v1/service/<name>', methods=['DELETE'])
def stop_service(name):
    return services.stop_service(name)

# Démarrage de l'API
if __name__ == '__main__':
    if config['debug']:
        app.run(host='127.0.0.1', port=int(config['port']))
    else:
        http_server = WSGIServer(('', int(config['port'])), app)
        http_server.serve_forever()