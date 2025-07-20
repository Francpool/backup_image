import functions_framework
import json
import os
from datetime import datetime
from flask import make_response

TEMP_FILE = '/tmp/requests.json'

@functions_framework.http
def store_image(request):
    # Manejo de CORS
    if request.method == 'OPTIONS':
        # Respuesta a preflight request
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    try:
        data = request.get_json()

        # Agrega status y timestamp
        data['status'] = 'incomplete'
        data['timestamp'] = datetime.utcnow().isoformat()

        # Lee archivo existente o crea uno nuevo
        if os.path.exists(TEMP_FILE):
            with open(TEMP_FILE, 'r') as f:
                content = json.load(f)
        else:
            content = []

        content.append(data)

        # Guarda de nuevo el archivo
        with open(TEMP_FILE, 'w') as f:
            json.dump(content, f)

        # Agrega encabezado CORS en la respuesta
        response = make_response('Request saved successfully.', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        response = make_response(f'Error: {str(e)}', 500)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
