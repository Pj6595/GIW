# -*- coding: utf-8 -*-

#
# Jaime Antolín, Álvar Domingo, Pablo Jurado, Leire Osés declaramos que esta
# solución es fruto exclusivamente de nuestro trabajo personal. No hemos sido ayudados por
# ninguna otra persona ni hemos obtenido la solución de fuentes externas, y tampoco hemos
# compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera
# deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar
# los resultados de los demás.
#

import hashlib
import os

import flask
from flask import Flask, request, session, make_response
import requests

app = Flask(__name__)

# Credenciales.
# https://developers.google.com/identity/protocols/oauth2/openid-connect#appsetup
# Copiar los valores adecuados.
CLIENT_ID = '668878841833-vi7e5q9dq44snv1mif8s27es9ov3atau.apps.googleusercontent.com'
CLIENT_SECRET = 'sX3G0hc5A2f0VZ0C3zaruIrS'

REDIRECT_URI = 'http://localhost:5000/token'

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el
# 'token endpoint'
# https://developers.google.com/identity/protocols/oauth2/openid-connect#authenticatingtheuser
DISCOVERY_DOC = 'https://accounts.google.com/.well-known/openid-configuration'
discoveryRequest = requests.get(DISCOVERY_DOC)
DISCOVERY_DOC_JSON = discoveryRequest.json()

# token_info endpoint para extraer información de los tokens en depuracion, sin
# descifrar en local
# https://developers.google.com/identity/protocols/OpenIDConnect#validatinganidtoken
TOKENINFO_ENDPOINT = 'https://oauth2.googleapis.com/tokeninfo'

#IMPORTANTE: Para acceder a la página de login, ir a la dirección http://localhost:5000/login_google con el servidor flask activo
@app.route('/login_google', methods=['GET'])
def login_google():
    #Creamos la clave de state y la guardamos en el diccionario session para que no se pierda el valor al salir de ámbito
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    session['state'] = state
    url = DISCOVERY_DOC_JSON["authorization_endpoint"] + "?client_id=" + CLIENT_ID + "&redirect_uri=" + REDIRECT_URI + "&scope=openid%20email&response_type=code&state=" + state
    response = make_response(flask.render_template('login_google.html', url = url))

    return response


@app.route('/token', methods=['GET'])
def token():
    #Comparamos la clave creada anteriormente con la que nos ha devuelto Google
    if request.args.get('state') != session['state']:
        return "Inicio de Sesión no valido", 400

    #Hacemos el post request al servidor de tokens
    data = {'code': request.args.get('code'),
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            'grant_type': 'authorization_code'}
    response = requests.post(DISCOVERY_DOC_JSON["token_endpoint"], data)
    token = response.json()['id_token']
    #Obtenemos la información del usuario con el endpoint de tokeninfo
    data_json = requests.get(TOKENINFO_ENDPOINT + "?id_token=" + token)
    data = data_json.json()
    return "Bienvenido " + data['email']


class FlaskConfig:
    '''Configuración de Flask'''
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = 'giw2020&!_()'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()

#░░░░░░░░██████████████████
#░░░░████░░░░░░░░░░░░░░░░░░████
#░░██░░░░░░░░░░░░░░░░░░░░░░░░░░██
#░░██░░░░░░░░░░Feliz Navidad░░░░░██
#██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
#██░░░░░░░░░░░░░░░░░░░░██████░░░░██
#██░░░░░░░░░░░░░░░░░░░░██████░░░░██
#██░░░░██████░░░░██░░░░██████░░░░██
#░░██░░░░░░░░░░██████░░░░░░░░░░██
#████░░██░░░░░░░░░░░░░░░░░░██░░████
#██░░░░██████████████████████░░░░██
#██░░░░░░██░░██░░██░░██░░██░░░░░░██
#░░████░░░░██████████████░░░░████
#░░░░░░████░░░░░░░░░░░░░░████
#░░░░░░░░░░██████████████