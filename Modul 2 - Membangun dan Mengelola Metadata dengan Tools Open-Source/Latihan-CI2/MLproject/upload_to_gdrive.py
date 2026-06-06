import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_folder_to_drive():
    # 1. Ambil rahasia dari GitHub Environment Variables
    creds_json = os.environ.get("GDRIVE_CREDENTIALS")
    folder_id = os.environ.get("GDRIVE_FOLDER_ID")
    
    if not creds_json or not folder_id:
        print("❌ Kredensial atau Folder ID tidak ditemukan di Environment!")
        return

    # 2. Login otomatis menggunakan Service Account
    info = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build("drive", "v3", credentials=creds)

    # 3. Cari file model.pkl di dalam folder mlruns lokal
    local_path = "mlruns/0"
    print("🔄 Mencari file model berukuran besar di folder lokal...")
    
    for root, dirs, files in os.walk(local_path):
        for file in files:
            if file == "model.pkl":
                full_path = os.path.join(root, file)
                print(f"📦 Menemukan file: {full_path}. Memulai proses upload ke Google Drive...")
                
                file_metadata = {
                    "name": f"credit_scoring_model_{os.path.basename(root)}.pkl",
                    "parents": [folder_id]
                }
                media = MediaFileUpload(full_path, mimetype="application/octet-stream", resumable=True)
                
                uploaded_file = service.files().create(
                    body=file_metadata, media_body=media, fields="id"
                ).execute()
                
                print(f" 🚀SELESAI! File sukses terupload dengan Drive ID: {uploaded_file.get('id')}")

if __name__ == "__main__":
    upload_folder_to_drive()