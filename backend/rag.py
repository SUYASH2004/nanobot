import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


DATA_DIR = "data"
METADATA_FILE = f"{DATA_DIR}/metadata.json"

with open(METADATA_FILE, "r", encoding="utf-8") as f:
    CHUNKS = json.load(f)


API_KEY = os.getenv("XAI_API_KEY")
if not API_KEY:
    raise ValueError("XAI_API_KEY not set in environment variables")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

GROK_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_top_k_chunks(query, k=5):
    """Naive substring search for top-k relevant chunks"""
    results = []
    query_lower = query.lower()
    for chunk in CHUNKS:
        if query_lower in chunk.lower():
            results.append(chunk)
        if len(results) >= k:
            break
    if not results:
        results = CHUNKS[:k]  
    return results

def answer_query(question, k=5):
    top_chunks = get_top_k_chunks(question, k)
    context = "\n\n".join(top_chunks)

    payload = {
        "model": "groq/compound",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for Flask documentation."},
            {"role": "user", "content": f"Answer the question based on the following context:\n{context}\n\nQuestion: {question}"}
        ]
    }

    response = requests.post(GROK_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"Grok API error: {response.status_code}, {response.text}")

    data = response.json()
    return data['choices'][0]['message']['content']
