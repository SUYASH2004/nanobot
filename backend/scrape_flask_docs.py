# scrape_flask_docs.py
import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://flask.palletsprojects.com/en/stable/"
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "flask_docs.json")
HEADERS = {"User-Agent": "Mozilla/5.0"}

# List of pages to scrape (main ones to avoid too many connection issues)
PAGES = [
    "",
    "quickstart/",
    "tutorial/",
    "installation/",
    "patterns/",
    "api/"
]

def fetch_page(session, url, retries=3, delay=2):
    """Fetch page content with retries"""
    for attempt in range(retries):
        try:
            res = session.get(url, timeout=10)
            res.raise_for_status()
            return res.text
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Attempt {attempt+1} failed for {url}: {e}")
            time.sleep(delay)
    print(f"❌ Skipping {url} after {retries} failed attempts")
    return None

def scrape_flask_docs():
    os.makedirs(DATA_DIR, exist_ok=True)
    session = requests.Session()
    session.headers.update(HEADERS)

    all_paragraphs = []

    for page in PAGES:
        url = urljoin(BASE_URL, page)
        print(f"📥 Fetching {url}...")
        html = fetch_page(session, url)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        all_paragraphs.extend(paragraphs)
        time.sleep(1)  # small delay to avoid hammering the server

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_paragraphs, f, ensure_ascii=False, indent=2)

    print(f"✅ Scraped {len(all_paragraphs)} paragraphs from Flask docs.")

if __name__ == "__main__":
    scrape_flask_docs()
