from flask import jsonify
from pony.orm import *
import response, subprocess, json
from entities import Favorite_service

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

@db_session
def search_favorite_services(name = ''):
    try:
        services = []
        raw_services = select(service for service in Favorite_service if (name in service.name)).order_by(Favorite_service.name)
        for service in raw_services:
            services.append({ 'name': service.name, 'serviceName': service.service_name })
        return jsonify({ 'status': 'OK', 'services': services }), 200
    except:
        return response.error_500()

@db_session
def create_favorite_service(service):
    try:
        # Récupèration du service depuis le corps de la requête
        raw_service = json.loads(service)

        # Récupèration du service existant
        current_service = Favorite_service.get(name = raw_service['name'])
        if current_service != None:
            return jsonify({ 'status': 'KO', 'message': 'Un service avec le nom \'' + raw_service['name'] + '\' existe déjà' }), 400

        # Vérification des champs obligatoires
        if ((not 'name' in raw_service) or (raw_service['name'].strip() == '')):
            return jsonify({ 'status': 'KO', 'message': 'Vous devez renseigner un nom (\'name\')' }), 400
        if ((not 'serviceName' in raw_service) or (raw_service['serviceName'].strip() == '')):
            return jsonify({ 'status': 'KO', 'message': 'Vous devez renseigner un nom de service (\'service_name\')' }), 400

        # Enregistrement du service
        service = Favorite_service(name = raw_service['name'], service_name = raw_service['serviceName'])
        commit()

        return jsonify({ 'status': 'OK' }), 201
    except:
       return response.error_500()
       
@db_session
def edit_favorite_service(name, service):
    try:
        # Récupèration du service existant
        current_service = Favorite_service.get(name = name)
        if current_service == None:
             return jsonify({ 'status': 'KO', 'message': 'Il n\'existe pas de service possèdant le nom \'' + str(name) + '\'' }), 400

        # Récupèration du service depuis le corps de la requête
        raw_service = json.loads(service)

        # Enregistrement du service
        if 'name' in raw_service and raw_service['name'].strip() != '':
            current_service.name = raw_service['name']
        if 'serviceName' in raw_service and raw_service['serviceName'].strip() != '':
            current_service.service_name = raw_service['serviceName']
        commit()

        return jsonify({ 'status': 'OK' }), 200
    except:
       return response.error_500()

@db_session
def delete_favorite_service(name):
    try:
        # Récupèration du service existant
        current_service = Favorite_service.get(name = name)
        if current_service == None:
             return jsonify({ 'status': 'KO', 'message': 'Il n\'existe pas de service possèdant le nom \'' + str(name) + '\'' }), 400

        # Suppression du service
        current_service.delete()

        return jsonify({ 'status': 'OK' }), 200
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