import firebase_admin, json, os
from firebase_admin import credentials, firestore

cred_path = os.getenv("FIREBASE_SA")
cred = credentials.Certificate(cred_path)
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
