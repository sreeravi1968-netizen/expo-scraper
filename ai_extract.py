import os, csv, requests, openai, json
from bs4 import BeautifulSoup
from googletrans import Translator
from langdetect import detect

openai.api_key = os.getenv("OPENAI_API_KEY")
translator = Translator()

CSV_PATH = "companies_with_sites.csv"

def fetch_text(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except:
        return None

def translate_to_english(text):
    if detect(text) != "en":
        return translator.translate(text, dest="en").text
    return text

def ai_extract(text):
    prompt = (
        "Extract the following as JSON:\n"
        "company, products (list), prices (list), description, contact info, website, images (list of URLs).\n"
        f"Website content:\n{text[:4000]}"
    )
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return resp['choices'][0]['message']['content']

def extract_all():
    structured_data = []
    with open(CSV_PATH, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in list(reader)[:100]:
            url = row.get("Website")
            if not url or url == "NOT FOUND":
                continue
            text = fetch_text(url)
            if not text:
                continue
            text_en = translate_to_english(text)
            json_data = ai_extract(text_en)
            try:
                obj = json.loads(json_data)
                # Ensure website key is always included
                obj['website'] = url
                structured_data.append(obj)
            except json.JSONDecodeError:
                print("AI returned invalid JSON for:", url)
    return structured_data
