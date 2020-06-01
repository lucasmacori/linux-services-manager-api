from flask import jsonify
import psutil
import response
import subprocess

def search_services():
    try:
        print(subprocess.run('who'))
        services = []
        for proc in psutil.process_iter(['name', 'pid']):
            services.append(proc.info)
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