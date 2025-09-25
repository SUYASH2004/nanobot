import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


DATA_DIR = "data"
BACKEND_DIR = Path(__file__).parent
METADATA_FILE = BACKEND_DIR / 'data' / 'metadata.json'

with open(METADATA_FILE, "r", encoding="utf-8") as f:
    CHUNKS = json.load(f)
import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Fix path and ensure file exists
BACKEND_DIR = Path(__file__).parent
DATA_DIR = BACKEND_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)  # Create directory if it doesn't exist

METADATA_FILE = DATA_DIR / 'metadata.json'

# Create file with empty data if it doesn't exist
if not METADATA_FILE.exists():
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)  # Initialize with empty list (since you're treating it as chunks)

# Now safely load the data
try:
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        CHUNKS = json.load(f)
except json.JSONDecodeError:
    # Handle case where file exists but is empty/corrupt
    CHUNKS = []

# If CHUNKS is empty, initialize with empty list
if not CHUNKS:
    CHUNKS = []

API_KEY = os.getenv("XAI_API_KEY")
if not API_KEY:
    raise ValueError("XAI_API_KEY not set in environment variables")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"  # Fixed typo: GROK_URL → GROQ_URL

def get_top_k_chunks(query, k=5):
    """Naive substring search for top-k relevant chunks"""
    # Handle case where CHUNKS might be empty
    if not CHUNKS:
        return ["No documentation chunks available. Please check if the data has been properly loaded."]
    
    results = []
    query_lower = query.lower()
    for chunk in CHUNKS:
        # Handle case where chunk might not be a string
        chunk_text = str(chunk) if not isinstance(chunk, str) else chunk
        if query_lower in chunk_text.lower():
            results.append(chunk_text)
        if len(results) >= k:
            break
    if not results:
        results = CHUNKS[:k]  
    return results

def answer_query(question, k=5):
    top_chunks = get_top_k_chunks(question, k)
    context = "\n\n".join(top_chunks)

    payload = {
        "model": "llama3-8b-8192",  # Fixed model name (groq/compound doesn't exist)
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for Flask documentation."},
            {"role": "user", "content": f"Answer the question based on the following context:\n{context}\n\nQuestion: {question}"}
        ],
        "max_tokens": 1000  # Added for safety
    }

    try:
        response = requests.post(GROQ_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()  # This will raise an exception for bad status codes
        
        data = response.json()
        return data['choices'][0]['message']['content']
    
    except requests.exceptions.RequestException as e:
        return f"Error calling Groq API: {str(e)}"
    except KeyError:
        return "Error: Unexpected response format from Groq API"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

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
