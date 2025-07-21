
# Google Cloud Image Backup App

## 🧩 Description

This project allows users to authenticate with Google, select an image, and back it up to their own Google Drive using Google Cloud Functions and Cloud Scheduler.

Este proyecto permite a los usuarios autenticarse con Google, seleccionar una imagen y respaldarla en su propio Google Drive usando Google Cloud Functions y Cloud Scheduler.

---

## 🚀 Components / Componentes

1. **Frontend**:
   - Authenticates with Google using OAuth2.
   - Sends image name, image (base64), user email, and access token to backend.

   - Se autentica con Google usando OAuth2.
   - Envía el nombre de la imagen, la imagen (base64), correo del usuario y token de acceso al backend.

2. **Cloud Function - `store_image`**:
   - Receives the data and stores it in `requests.json` in temporary storage with status `incomplete`.

   - Recibe los datos y los guarda en `requests.json` en almacenamiento temporal con estado `incomplete`.

3. **Cloud Function - `process_requests`**:
   - Periodically reads `requests.json` and uploads the image to user's Google Drive using the saved token.

   - Lee periódicamente `requests.json` y sube la imagen al Google Drive del usuario usando el token guardado.

4. **Cloud Scheduler**:
   - Triggers `process_requests` every 5 minutes.

   - Dispara `process_requests` cada 5 minutos.

---

## ⚙️ Setup Instructions / Instrucciones de configuración

### 🔐 Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable:
   - Google Drive API
   - OAuth 2.0 Client ID (Web Application)
3. Use your `CLIENT_ID` in the HTML file.

---

### ☁️ Deploy Functions / Desplegar Funciones

```bash
gcloud functions deploy store_image \
    --runtime python310 \
    --trigger-http \
    --entry-point store_image \
    --source ./store_image_function \
    --allow-unauthenticated

gcloud functions deploy process_requests \
    --runtime python310 \
    --trigger-http \
    --entry-point process_requests \
    --source ./process_requests_function \
    --allow-unauthenticated
```

---

### ⏰ Cloud Scheduler

```bash
gcloud scheduler jobs create http trigger-process-requests \
    --schedule "*/5 * * * *" \
    --uri "https://REGION-PROJECT.cloudfunctions.net/process_requests" \
    --http-method POST \
    --time-zone "America/Vancouver"
```

---

## 🌐 Frontend

Edit `frontend_google_drive_backup.html`:
- Replace `YOUR_GOOGLE_CLIENT_ID_auth`
- Replace `https://REGION-PROJECT.cloudfunctions.net/store_image`

---

## ✅ Requirements / Requisitos

- Google Cloud SDK
- Python 3.10
- Google Cloud project with billing enabled
- APIs enabled: Google Drive, Cloud Functions, Cloud Scheduler

---

## 📁 Files / Archivos

- `store_image_function/`: Saves incoming requests
- `process_requests_function/`: Processes and uploads to Drive
- `frontend_google_drive_backup.html`: Web UI

---

## 👤 Author

Developed by request for Google Cloud Function integration in Python.

Desarrollado por solicitud para una integración de Google Cloud Function en Python.


--------------------------------------------------------------------------------------------------------
# Google Drive Image Backup with Cloud Functions

This project enables users to authenticate with Google, upload an image via a frontend,
store the request in Cloud Storage, and process it via Cloud Functions to upload it to Google Drive.

## Setup Steps

### 1. Enable APIs
```bash
gcloud services enable drive.googleapis.com
gcloud services enable storage.googleapis.com
```

### 2. Create Cloud Storage Bucket
```bash
gsutil mb gs://backup-images-vancouver
```

### 3. OAuth 2.0 Credentials
Create OAuth 2.0 client ID (Web type) in Google Cloud Console and allow JS origin (e.g., http://localhost).

### 4. Deploy `store_image` Function
```bash
gcloud functions deploy store_image \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point store_image \
  --source store_image_function
```

### 5. Deploy `process_requests` Function
```bash
gcloud functions deploy process_requests \
  --runtime python310 \
  --trigger-http \
  --entry-point process_requests \
  --source process_requests_function \
  --allow-unauthenticated
```
Trigger manually:
```bash
curl -X POST -d '' https://REGION-PROJECT_ID.cloudfunctions.net/process_requests
```

### 6. Frontend HTML Sample
Include Google OAuth JS client and use `fetch` to send payload to Cloud Function.

### 7. Verify
```bash
gcloud functions logs read process_requests --limit=10
gsutil cat gs://backup-images-vancouver/requests.json
```
