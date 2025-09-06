import firebase_admin
import json
import os
from firebase_admin import credentials, firestore

# Load Firebase credentials from environment
cred_path = os.getenv("FIREBASE_SA")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_all(structured_data):
    """
    Upload only clean company data to Firestore.
    """
    for obj in structured_data:
        try:
            # Handle if obj is JSON string instead of dict
            if isinstance(obj, str):
                obj = json.loads(obj)

            company_name = obj.get("company", "").strip()

            # Skip if company name missing
            if not company_name:
                print(f"Skipping company with no name for URL: {obj.get('website')}")
                continue

            # Only keep required fields
            clean_obj = {
                "company": company_name,
                "website": obj.get("website", ""),
                "products": obj.get("products", []),
                "prices": obj.get("prices", []),
                "description": obj.get("description", ""),
                "contact": obj.get("contact", ""),
                "images": obj.get("images", [])
            }

            # Upload using company name as document ID
            db.collection("companies_pre_expo").document(company_name).set(clean_obj)
            print(f"Uploaded clean data for: {company_name}")

        except Exception as e:
            print("Upload error:", e)
