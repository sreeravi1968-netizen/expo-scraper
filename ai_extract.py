import os
import csv
import requests
import openai
import json
from bs4 import BeautifulSoup
from googletrans import Translator
from langdetect import detect

openai.api_key = os.getenv("OPENAI_API_KEY")
translator = Translator()

CSV_PATH = "companies_with_sites.csv"

def fetch_text(url):
    """Fetch raw text from a website URL using BeautifulSoup."""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except:
        return None

def translate_to_english(text):
    """Translate text to English if detected language is not English."""
    try:
        if detect(text) != "en":
            return translator.translate(text, dest="en").text
    except:
        pass
    return text

def ai_extract(text):
    """Send text to OpenAI and return JSON string with structured data."""
    prompt = (
        "You are an expert data extractor. Extract the following as JSON:\n"
        "- company (string)\n"
        "- products (list of strings)\n"
        "- prices (list of strings)\n"
        "- description (string)\n"
        "- contact (string)\n"
        "- website (string)\n"
        "- images (list of URLs)\n\n"
        f"Website content:\n{text[:4000]}\n\n"
        "Return valid JSON only, do not include extra text."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return resp['choices'][0]['message']['content']

def chunk_text(text, size=4000):
    """Split long text into chunks of 4000 characters."""
    return [text[i:i+size] for i in range(0, len(text), size)]

def extract_all():
    """Read CSV, scrape websites, extract structured data via AI, and return a list of dicts."""
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

            # Initialize merged result
            merged = {
                "company": "",
                "products": [],
                "prices": [],
                "description": "",
                "contact": "",
                "images": [],
                "website": url
            }

            # Split text into chunks to ensure all content is processed
            chunks = chunk_text(text_en)
            for c in chunks:
                json_data = ai_extract(c)
                try:
                    obj = json.loads(json_data)
                    merged["company"] = obj.get("company", merged["company"])
                    merged["products"].extend(obj.get("products", []))
                    merged["prices"].extend(obj.get("prices", []))
                    merged["description"] += " " + obj.get("description", "")
                    merged["contact"] = obj.get("contact", merged["contact"])
                    merged["images"].extend(obj.get("images", []))
                except json.JSONDecodeError:
                    print("AI returned invalid JSON for:", url)
                    continue

            # Remove duplicates and clean lists
            merged["products"] = list(set(merged["products"]))
            merged["prices"] = list(set(merged["prices"]))
            merged["images"] = list(set(merged["images"]))
            merged["description"] = merged["description"].strip()

            structured_data.append(merged)

    return structured_data
