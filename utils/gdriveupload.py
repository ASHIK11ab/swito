import requests
import io
import googleapiclient.discovery
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
from flask import current_app as app
from werkzeug.utils import secure_filename

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'swito-google-creds.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

drive_service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)

def upload_file(file, category):
  filename = secure_filename(file.filename)
  extension = filename.rsplit('.')[1]

  file_metadata = {
    'name': filename,
    'parents': [app.config[f"{category}_UPLOAD_DIRECTORY"]]
  }
  file_bytes_data = io.BytesIO(file.read())
  # Body of request which contains the file data.
  media = MediaIoBaseUpload(file_bytes_data, mimetype=f'image/{extension}')
  resp = drive_service.files().create(body=file_metadata,
                                      media_body=media,
                                      ).execute()
  if 'id' not in resp.keys():
    return (False, None)
  image_url = f"https://drive.google.com/uc?export=view&id={resp['id']}"
  return (True, image_url)