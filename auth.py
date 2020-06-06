from flask import jsonify
from pony.orm import *
from entities import User, Token
import hashlib

def login(username, password):
    # Récupèration de l'utilisateur
    user = User.get(name = username)
    if user == None:
        return jsonify({ 'status': 'KO', 'message': 'Mauvais nom d\'utilisateur ou mot de passe' }), 400
    
    # Vérification du mot de passe
    