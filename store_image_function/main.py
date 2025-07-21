import functions_framework
import json
import os
from datetime import datetime
from flask import make_response
from google.cloud import storage  # Asegúrate que está en requirements.txt

TEMP_FILE = '/tmp/requests.json'
BUCKET_NAME = 'backup-images-vancouver'
DEST_BLOB_NAME = 'requests.json'

@functions_framework.http
def store_image(request):
    # Manejo de CORS
    if request.method == 'OPTIONS':
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

        # Leer archivo existente
        if os.path.exists(TEMP_FILE):
            with open(TEMP_FILE, 'r') as f:
                content = json.load(f)
        else:
            content = []

        content.append(data)

        # Guardar de nuevo
        with open(TEMP_FILE, 'w') as f:
            json.dump(content, f)

        # Subir a Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(DEST_BLOB_NAME)
        blob.upload_from_filename(TEMP_FILE, content_type='application/json')

        response = make_response('✅ Request saved and uploaded successfully.', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        response = make_response(f'❌ Error: {str(e)}', 500)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
