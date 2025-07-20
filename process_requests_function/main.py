
import json
import os
import requests

TEMP_FILE = '/tmp/requests.json'
UPLOAD_URL = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart'

def process_requests(request):
    if not os.path.exists(TEMP_FILE):
        return 'No pending requests.', 200

    with open(TEMP_FILE, 'r') as f:
        requests_data = json.load(f)

    updated_requests = []

    for item in requests_data:
        if item['status'] == 'incomplete':
            access_token = item['google_drive_token']
            image_data = item['image']
            image_name = item['image_name']

            try:
                image_bytes = image_data.encode("utf-8")  # Reemplazar por base64.b64decode si es necesario

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
                    item['status'] = 'completed'
                else:
                    item['status'] = 'error'
                    item['error_message'] = response.text
            except Exception as e:
                item['status'] = 'error'
                item['error_message'] = str(e)

        updated_requests.append(item)

    with open(TEMP_FILE, 'w') as f:
        json.dump(updated_requests, f)

    return 'Processing completed.', 200
