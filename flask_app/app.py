import requests
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)


# creamos una ruta base para la aplicación
@app.route("/")
def hello_world():
    return "Hola mundo! :)"


# disponibilizamos un punto de entrada a la aplicación que acepta solicitudes de tipo
# POST. Notar que no acepta solicitudes tipo GET, pues no se le indica
@app.route('/post_endpoint', methods=["POST"])
def post_endpoint():
    # intenta obtener un JSON que venga en el contenido de la solicitud
    try:
        input_json = request.get_json()
        # intenta buscar una clave "text" en el JSON
        input_text = input_json.get("text", None)
    except AttributeError:
        # si no viene un JSON en la solicitud, entonces carga esto
        input_text = "Ni un JSON :c"
    
    if not input_text:
        # si no existe el campo "text" en el JSON, entonces carga esto
        input_text = "Nada :("
    response = {'Recibí: ': input_text}

    # retornamos la respuesta como un JSON, puesto que se había definido como un
    # dicccionario de Python (jsonify lo pasa de dict a JSON)
    return jsonify(response)


@app.route('/get_data_from_url', methods=["POST"])
def get_data_from_url():
    """
    Intenta acceder a una URL entregada en un JSON. Si la encuentra, devuelve el largo
    de su contenido y sus primeros 250 caracteres.
    """
    try:
        input_json = request.get_json()
        input_url = input_json.get("url", None)
    except AttributeError:
        response_text = "JSON vacío"
        response = {"Error": response_text}
        return jsonify(response)
    
    if not input_url:
        input_url = "Nada :("
        response = {"Error": "JSON no contiene campo URL"}
        return jsonify(response)

    # usamos librería requests para enviar una solicitud a un sitio externo
    # el ".text" hará que la respuesta recibida se cargue como texto
    url_content = requests.get(input_url).text
    response = {
        "Principio del contenido: ": url_content[:250],
        "Largo del contenido": len(url_content)
    }

    return jsonify(response)


@app.route('/post_get_santiago_time', methods=["POST"])
def post_get_santiago_time():
    """Llama a una API externa y devuelve la información que esta entrega.

    Nota: solo permite solicitudes tipo POST (no se puede acceder en un navegador)
    """
    api_endpoint = "http://worldtimeapi.org/api/timezone/America/Santiago"
    # usamos librería requests para enviar una solicitud a un sitio externo
    # el ".json()" hace que se busque un JSON en el contenido de la respuesta y se
    # carga como tal en caso de existir, sino, la solicitud fallaría
    time_data = requests.get(api_endpoint).json()

    response = {"Datos de la hora en Santiago": time_data}

    return jsonify(response)


@app.route('/get_santiago_time', methods=["GET"])
def get_santiago_time():
    """Llama a una API externa y devuelve la información que esta entrega.

    Nota: permite solicitudes tipo GET (se puede acceder en un navegador)
    """
    api_endpoint = "http://worldtimeapi.org/api/timezone/America/Santiago"
    time_data = requests.get(api_endpoint).json()

    response = {"Datos de la hora en Santiago": time_data}

    return jsonify(response)


@app.route("/load_template")
def load_template():
    """Carga un template, entregándole un valor a mostrar"""
    return render_template("index.html", content="Hola!")
