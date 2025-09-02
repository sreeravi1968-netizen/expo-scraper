from ai_extract import extract_all
from upload_firebase import upload_all

def main():
    structured_data = extract_all()
    upload_all(structured_data)

if __name__ == "__main__":
    main()
