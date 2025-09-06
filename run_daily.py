from ai_extract import extract_all
from upload_firebase import upload_all

def main():
    print("Extracting data from CSV and websites...")
    structured_data = extract_all()

    # Debug: print first 2 records to verify
    print("Sample extracted data:")
    for item in structured_data[:2]:
        print(item)

    print("Uploading to Firebase...")
    upload_all(structured_data)
    print("Upload complete.")

if __name__ == "__main__":
    main()
