# -*- coding: utf-8 -*-

#
# Jaime Antolín, Álvar Domingo, Pablo Jurado, Leire Osés y Sans Undertale declaramos que esta solución es fruto exclusivamente
#de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
#obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
#con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
#actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
#


from flask import Flask, request, session, render_template, send_file
from mongoengine import connect, Document, StringField, EmailField, BinaryField
import hashlib, random, string
import bcrypt, pyotp, qrcode

# Resto de importaciones

app = Flask(__name__)
connect('giw_auth')


# Clase para almacenar usuarios usando mongoengine
class User(Document):
    user_id = StringField(primary_key=True)
    full_name = StringField(min_length=2, max_length=50, required=True)
    country = StringField(min_length=2, max_length=50, required=True)
    email = EmailField(required=True)
    passwd = BinaryField(required=True)
    totp_secret = StringField(required=False)

def hashearPassword(password, salt = None):
    if salt == None:
        salt = bcrypt.gensalt()
    hashedPass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashedPass


##############
# APARTADO 1 #
##############

# 
# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro
#


@app.route('/signup', methods=['POST'])
def signup():
    nickname = request.form['nickname']
    nombre = request.form['full_name'] 
    pais = request.form['country']
    mail = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']
    usuario = User.objects(user_id = nickname).first()

    if usuario != None:
        return "El usuario ya existe crack", 400

    if password != password2:
        return "Las contraseñas no coinciden", 400

    hashedPass = hashearPassword(password)
    
    nuevoUsuario =  User(user_id=nickname, full_name=nombre, country=pais, email=mail, passwd=hashedPass)
    
    try:
        nuevoUsuario.save()
    except:
        return "No has introducido bien los datos", 400
    return "Bienvenido usuario " + nombre, 200


@app.route('/change_password', methods=['POST'])
def change_password():
    nickname = request.form["nickname"]
    old_pasword = request.form["old_password"]
    new_password = request.form["new_password"]

    if(nickname != None and old_pasword != None and new_password != None):
        usuario_bd = User.objects(user_id =nickname).first()

        correcto = usuario_bd != None

        if correcto:
            correcto = bcrypt.checkpw(old_pasword.encode('utf-8'), usuario_bd.passwd)

        if(correcto):
            usuario_bd.passwd = hashearPassword(new_password)
            usuario_bd.save()
            return "La contrasena del usuario " +  nickname + " ha sido modificada"
        else:
            return "No existe usuario o la contraseña es incorrecta", 400  
    else:
         return "No se han introducido los parametros correctamente", 400
 
           
@app.route('/login', methods=['POST'])
def login():
    nickname = request.form["nickname"]
    password = request.form["password"]

    usuario = User.objects(user_id =nickname).first()
    if usuario == None or not bcrypt.checkpw(password.encode('utf-8'), usuario.passwd):
        return "Usuario o contraseña incorrectos", 400
    return "Bienvenido " + usuario.full_name, 200
    

##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    nickname = request.form['nickname']
    nombre = request.form['full_name'] 
    pais = request.form['country']
    mail = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']
    usuario = User.objects(user_id = nickname).first()

    if usuario != None:
        return "El usuario ya existe crack", 400

    if password != password2:
        return "Las contraseñas no coinciden", 400

    hashedPass = hashearPassword(password)
    totp_s = pyotp.random_base32()
    
    nuevoUsuario =  User(user_id=nickname, full_name=nombre, country=pais, email=mail, passwd=hashedPass, totp_secret = totp_s)
    try:
        nuevoUsuario.save()
        totpUrl = pyotp.totp.TOTP(nuevoUsuario.totp_secret).provisioning_uri(name=nuevoUsuario.user_id, issuer_name='TOTP para GIW')
        img = qrcode.make(totpUrl)
        img.save('totpqr.png')
    except:
        return "No has introducido bien los datos", 400
    return send_file('totpqr.png'), 200
        

@app.route('/login_totp', methods=['POST'])
def login_totp():
    userTotp = request.form["totp"]
    nickname = request.form["nickname"]
    password = request.form["password"]

    usuario = User.objects(user_id =nickname).first()
    if usuario == None or not bcrypt.checkpw(password.encode('utf-8'), usuario.passwd):
        return "Usuario o contraseña incorrectos", 400

    userTotp_check = pyotp.TOTP(usuario.totp_secret)
    if userTotp_check.verify(userTotp):
        return "Bienvenido usuario " + usuario.full_name, 200
    else:
        return "Clave TOTP incorrecta", 400
  

class FlaskConfig:
    """Configuración de Flask"""
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = "giw2020&!_()"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()
