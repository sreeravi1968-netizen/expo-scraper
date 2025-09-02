def upload_all(structured_data):
    for data in structured_data:
        try:
            obj = json.loads(data) if isinstance(data, str) else data
            company_name = obj.get("company", "").strip()
            
            # Skip if company name is empty
            if not company_name:
                print("Skipping company with no name:", obj.get("website"))
                continue

            # Only keep required fields
            clean_obj = {
                "company": company_name,
                "website": obj.get("website"),
                "products": obj.get("products", []),
                "prices": obj.get("prices", []),
                "description": obj.get("description", ""),
                "contact": obj.get("contact", ""),
                "images": obj.get("images", [])
            }

            db.collection("companies_pre_expo").document(company_name).set(clean_obj)
        except Exception as e:
            print("Upload error:", e)
