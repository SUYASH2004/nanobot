import os
from playwright.sync_api import sync_playwright

# Data folder
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# List of docs to scrape
DOCS = {
    "flask": "https://flask.palletsprojects.com/en/2.3.x/",
    "fastapi": "https://fastapi.tiangolo.com/",
    "streamlit": "https://docs.streamlit.io/"
}

def scrape_site(url):
    """Scrape all paragraphs from a site using Playwright."""
    text_content = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # Extract all paragraphs
        paragraphs = page.locator("p").all_text_contents()
        text_content.extend(paragraphs)
        
        browser.close()
    return text_content

def save_to_file(name, content):
    """Save scraped content to .txt file"""
    file_path = os.path.join(DATA_FOLDER, f"{name}_docs.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(content))
    print(f"Saved: {file_path}")

# Scrape each doc
for name, url in DOCS.items():
    print(f"Scraping {name} docs...")
    content = scrape_site(url)
    save_to_file(name, content)
