import os
import requests
from dotenv import load_dotenv

# Load your .env variables
load_dotenv()
API_KEY = os.getenv("XAI_API_KEY")

if not API_KEY:
    raise ValueError("XAI_API_KEY not set!")

# Grok models endpoint
url = "https://api.groq.com/openai/v1/models"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
print("Response:")
print(response.text)
