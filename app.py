from flask import Flask
import services

# Création de l'application web
app = Flask(__name__)

# Définition des routes de l'API
@app.route('/api/v1/services', methods=['GET'])
def get_service():
    return services.search_services()

@app.route('/api/v1/service/<name>', methods=['PUT'])
def start_service(name):
    return services.start_service(name)

# Démarrage de l'API
if __name__ == '__main__':
    app.run()