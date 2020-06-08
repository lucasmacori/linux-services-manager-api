from flask import jsonify
from pony.orm import *
from entities import User, Token
import bcrypt, response, json
from secrets import token_urlsafe

@db_session
def login(user_request):
    try:
        # Récupèration de l'authentification depuis le corps de la requête                   
        user_request = json.loads(user_request)

        # Vérification des champs obligatoires
        if ((not 'username' in user_request) or (user_request['username'].strip() == '')):
            return jsonify({ 'status': 'KO', 'message': 'Vous devez renseigner un nom d\'utilisateur (\'username\')' }), 400
        if ((not 'password' in user_request) or (user_request['password'].strip() == '')):
            return jsonify({ 'status': 'KO', 'message': 'Vous devez renseigner un mot de passe (\'password\')' }), 400

        username = user_request['username']
        password = user_request['password']

        # Récupèration de l'utilisateur
        user = User.get(name = username)
        if user == None:
            return jsonify({ 'status': 'KO', 'message': 'Mauvais nom d\'utilisateur ou mot de passe' }), 400

        # Vérification du mot de passe
        if bcrypt.hashpw(password, user.hash) == user.hash:
            # Utilisateur authentifié

            # Vérification de l'existence d'un ancien token
            token = Token.get(user = user)
            if user != None:
                token.delete()

            # Création d'un nouveau token
            token = Token(user = user, token = token_urlsafe(32))
            commit()
            return jsonify({ 'status': 'OK', 'token': token.token }), 200
        else:
            return jsonify({ 'status': 'KO', 'message': 'Mauvais nom d\'utilisateur ou mot de passe' }), 400
    except:
        return response.error_500()

@db_session
def check_token(username, token):
    try:
        # Vérification des champs obligatoires
        if username == None or username.strip() == '':
            return False, jsonify({ 'status': 'KO', 'message': 'Vous devez renseigner un nom d\'utilisateur dans l\'entête de la requête (\'username\')' }), 401
        if token == None or token.strip() == '':
            return False, jsonify({ 'status': 'KO', 'message': 'Vous devez renseigner un token dans l\'entête de la requête (\'token\')' }), 401

        # Vérification de l'existence de l'utilisateur
        user = User.get(name = username)
        if user == None:
            return False, 'Le token est invalide'
        else:
            token = Token.get(user = user, token = token)
            if token == None:
                return False, jsonify({ 'status': 'KO', 'message': 'Le token est invalide' }), 401
        return True, None, None
    except:
        return False, jsonify({ 'status': 'KO', 'message': 'Une erreur inattendue est survenue' }), 500