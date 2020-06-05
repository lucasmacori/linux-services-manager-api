from gevent.pywsgi import WSGIServer
from flask import Flask
import services


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

@app.route('/api/v1/service/<name>', methods=['PUT'])
def start_service(name):
    return services.start_service(name)
    
@app.route('/api/v1/service/<name>', methods=['DELETE'])
def stop_service(name):
    return services.stop_service(name)

# Démarrage de l'API
if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()