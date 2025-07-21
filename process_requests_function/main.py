import json
import base64
import requests
from google.cloud import storage
import os

BUCKET_NAME = 'backup-images-vancouver'
REQUEST_FILE_NAME = 'requests.json'
UPLOAD_URL = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart'

def process_requests(request):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(REQUEST_FILE_NAME)

    if not blob.exists():
        return 'No requests.json file found in bucket.', 200

    # Descargar y leer requests.json
    data_bytes = blob.download_as_bytes()
    try:
        requests_data = json.loads(data_bytes.decode('utf-8'))
    except Exception as e:
        return f'Error parsing JSON: {e}', 500

    updated_requests = []

    for item in requests_data:
        # Procesar solo los que están pendientes
        if item.get('status') != 'incomplete':
            updated_requests.append(item)
            continue

        access_token = item.get('google_drive_token')
        image_data = item.get('image')
        image_name = item.get('image_name')

        try:
            image_bytes = base64.b64decode(image_data)

            files = {
                'metadata': ('metadata', json.dumps({
                    'name': image_name,
                    'mimeType': 'image/jpeg'
                }), 'application/json'),
                'file': ('image.jpg', image_bytes, 'image/jpeg')
            }

            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post(UPLOAD_URL, headers=headers, files=files)

            if response.status_code in [200, 201]:
                response_data = response.json()
                item['status'] = 'completed'
                item['file_id'] = response_data.get('id')
                item['drive_link'] = f"https://drive.google.com/file/d/{item['file_id']}/view"
            else:
                item['status'] = 'error'
                item['error_message'] = response.text

        except Exception as e:
            item['status'] = 'error'
            item['error_message'] = str(e)

        updated_requests.append(item)

    # Guardar requests.json actualizado en el bucket
    try:
        blob.upload_from_string(json.dumps(updated_requests, indent=2), content_type='application/json')
    except Exception as e:
        return f'Error uploading updated requests.json: {e}', 500

    return 'Processing completed.', 200
