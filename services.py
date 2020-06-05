from flask import jsonify
from classes.service import Service
import response
import subprocess

#
# Méthodes de module
#

def list_services(name = None):
    '''
    Liste les services activés sur le système
    @param name: Nom de service à rechercher. Ce paramètre est optionnel. S'il n'est pas renseigné, tous les services sont renvoyés
    '''
    # Récupération des services via systemctl
    p = subprocess.Popen(['systemctl', '--type=service', '--all', '--no-legend', '--no-pager'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()

    # Découpage des résultats
    output = str(output)
    raw_services = []
    splited_output = output.replace('\\n', ' ').split()
    for i in range(0, len(splited_output), 1):
        element = str(splited_output[i])
        if element.endswith('.service'):
            if i > 0:
                # Le service est découpé, ajout à la liste et passage au suivant
                current_service['name'] = current_service['name'][0:-len('.service')]
                current_service['description'] = current_service['description'][1:]
                raw_services.append(current_service)
            count = 0
            current_service = { 'name': element, 'description': '' }
        else:
            # Récupération des différents champs
            if count == 0:
                current_service['loaded'] = (element == 'loaded')
            elif count == 1:
                current_service['active'] = (element == 'active')
            elif count == 2:
                current_service['sub'] = element
            else:
                current_service['description'] = current_service['description'] + ' ' + element
            count += 1

    # Tri des services
    services = []
    for service in raw_services:
        if (name == None or name in str(service['name'])):
            services.append(service)
    return services

#
# Controlleurs
#

def search_services(name = None):
    try:
        services = list_services(name)
        return jsonify({ 'status': 'OK', 'services': services }), 200
    except:
        return response.error_500()

def search_favorite_services(name = None):
    try:
        services = list_services(name)
        return jsonify({ 'status': 'OK', 'services': services }), 200
    except:
        return response.error_500()


def toggle_service(name, action):
    try:
        result = subprocess.run(['systemctl', action, name])
        if (result.returncode == 0):
            return jsonify({ 'status': 'OK' }), 200
        elif (result.returncode == 5):
            message = 'Le service ' + str(name) + ' n\'existe pas'
            return jsonify({ 'status': 'KO', 'message': message }), 400
        else:
            raise ValueError('Erreur inconnue')
    except:
        return response.error_500()
        
def start_service(name):
    return toggle_service(name, 'start')
    
def stop_service(name):
    return toggle_service(name, 'stop')