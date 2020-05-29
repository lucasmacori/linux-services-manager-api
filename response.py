from flask import jsonify

def error_400(error='La requête est incorrecte'):
    data = {'message': error}
    return jsonify(data), 400

def error_401(error='Vous n\'êtes pas autorisé à affectuer cette action'):
    data = {'message': error}
    return jsonify(data), 400


def error_500(error='Une erreur inattendue est survenue'):
    data = {'message': error}
    return jsonify(data), 500