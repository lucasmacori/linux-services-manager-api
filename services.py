from flask import jsonify
import psutil
import response
import subprocess

def search_services():
    services = []
    for proc in psutil.process_iter(['pid', 'name']):
        services.append(proc.info)
    return jsonify({ 'services': services }), 200

def start_service(name):
    result = subprocess.call('sudo systemctl start name')
    print(result)