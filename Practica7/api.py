"""
GIW 2020-21
Práctica 07
Grupo 06
Autores: Jaime Antolín, Álvar Domingo, Pablo Jurado, Leire Osés

Jaime Antolín, Álvar Domingo, Pablo Jurado y Leire Osés declaramos que esta solución es fruto exclusivamente
de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
"""
from flask import Flask, request, session, render_template
from flask import jsonify
app = Flask(__name__)

listaAsignaturas = []

def compruebaRequest(requestData):
    return {"nombre","numero_alumnos", "horario"} <= requestData.keys() and type(requestData["nombre"]) == str and type(requestData["numero_alumnos"]) == int and type(requestData["horario"]) == list and len(requestData.keys()) == 3

@app.route('/', methods=['GET'])
def root():
    """/ es una ruta válida"""
    return 'Soy la página principal'

def rutas_asig_gte(list_asignturas, umbral):
    """Devuelve el conjunto de rutas de las asignaturas que tienen más o igual número de alumnos"""
    gte = filter(lambda x: x['numero_alumnos'] >= umbral, list_asignturas)
    return list(map(lambda x: f"/asignaturas/{x['id']}", gte))


def rutas_paginado(list_asignturas, per_page, page):
    """Devuelve el conjunto de rutas de las asignaturas considerando la paginación"""
    asigs = list_asignturas[(page - 1) * per_page:page * per_page]
    return list(map(lambda x: f"/asignaturas/{x['id']}", asigs))

@app.route('/asignaturas', methods=['GET'])
def asignaturas():
    asignaturasUrls = []
    result = {}
    result["asignaturas"] = asignaturasUrls

    if len(listaAsignaturas) == 0:
        return result, 200

    if(len(request.args) == 0):
        for elem in listaAsignaturas:
            asignaturasUrls.append("/asignaturas/" + str(elem["id"]))

        return result, 200

    alumnos_gte = request.args.get("alumnos_gte", None, int)
    page = request.args.get("page", None, int)
    per_page = request.args.get("per_page", None, int)

    #Paginado sin filtro
    if page != None and per_page != None and alumnos_gte == None:
        asignaturasUrls = rutas_paginado(listaAsignaturas, per_page, page)

    #Paginado con filtro
    elif page != None and per_page != None and alumnos_gte != None:
        asignaturasFiltradas = []
        for i in listaAsignaturas:
            if i["numero_alumnos"] >= alumnos_gte:
                asignaturasFiltradas.append(i)

        asignaturasUrls = rutas_paginado(asignaturasFiltradas, per_page, page)

    #no existe ninguno de los parámetros de filtrado
    elif alumnos_gte == None:
        return "Parámetros introducidos no válidos", 400
    #solo existe alumnos_gte
    else:
        asignaturasUrls = rutas_asig_gte(listaAsignaturas, alumnos_gte)

    result["asignaturas"] = asignaturasUrls
    if len(asignaturasUrls) == len(listaAsignaturas):
        return result, 200
    else:
        return result, 206

@app.route('/asignaturas', methods=['DELETE'])
def borrarAsignaturas():
    listaAsignaturas.clear()
    return 'Todas las asignaturas han sido borradas',204

@app.route('/asignaturas', methods=['POST'])
def anadeAsignaturas():
    requestData = request.get_json()
    if requestData == None:
        return 'Formato no aceptado', 400
    
    if compruebaRequest(requestData):
        idNum = len(listaAsignaturas)
        listaAsignaturas.append(requestData)
        listaAsignaturas[idNum]["id"] = idNum
        return {"id": idNum}, 201
    else:
        return 'Formato no aceptado json incorrecto', 400

@app.route('/asignaturas/<int:numero>', methods=['DELETE'])
def borrarAsignatura(numero):
    if numero >= len(listaAsignaturas) or numero < 0:
        return 'Not Found', 404

    listaAsignaturas.remove(listaAsignaturas[numero])
    for i in range(numero, len(listaAsignaturas)):
        listaAsignaturas[i]["id"]-=1

    return 'Todas las asignaturas han sido borradas',204

@app.route('/asignaturas/<int:numero>', methods=['GET'])
def obtenerAsignatura(numero):
    if numero < len(listaAsignaturas):
        return listaAsignaturas[numero], 200
    else:
         return "Asignatura no encontrada", 404

@app.route('/asignaturas/<int:numero>', methods=['PUT'])
def reemplazarAsignatura(numero):
    if numero >= len(listaAsignaturas) or numero < 0:
        return "Asignatura no encontrada", 404

    requestData = request.get_json()
    if requestData == None:
        return 'Formato no aceptado', 400
    
    if compruebaRequest(requestData):
        listaAsignaturas[numero] = requestData
        listaAsignaturas[numero]["id"] = numero
        return listaAsignaturas[numero], 200
    else:
        return 'Formato no aceptado json incorrecto', 400
    
    

@app.route('/asignaturas/<int:numero>', methods=['PATCH'])
def modificaCampoAsignatura(numero):

    if numero < len(listaAsignaturas):
        requestData = request.get_json()
        if requestData == None:
            return 'Formato no aceptado, solo JSON valido', 400
    
        if(len(requestData)>1):
            return "Demasiados parametros, introducir solo 1", 400

        key = list(requestData.keys())[0]
        if "nombre" == key or key =="numero_alumnos" or key == "horario":
            listaAsignaturas[numero][key] = requestData[key]
            return "Campo modificado", 200
        else:
            return "Campo no válido", 400
        
    else:
         return "Asignatura no encontrada", 404

       
@app.route('/asignaturas/<int:numero>/horario', methods=['GET'])
def getHorario(numero):
    if numero >= len(listaAsignaturas) or numero < 0:
        return 'Not Found', 404

    result = {}
    result["horario"] = listaAsignaturas[numero]["horario"]

    return result, 200

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

