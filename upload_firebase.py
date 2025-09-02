# Write the secret JSON string to a temporary file
firebase_json = os.getenv("FIREBASE_SA")
with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
    f.write(firebase_json)
    temp_path = f.name

cred = credentials.Certificate(temp_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_all(structured_data):
    for data in structured_data:
        try:
            obj = json.loads(data)
            company_name = obj.get("company")
            if company_name:
                db.collection("companies_pre_expo").document(company_name).set(obj)
        except Exception as e:
            print("Upload error:", e)
import firebase_admin, json, os, tempfile
from firebase_admin import credentials, firestore

