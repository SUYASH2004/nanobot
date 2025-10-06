from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

# Initialize retriever (commented out for now to test basic functionality)
# retriever = DocRetriever()

@app.get("/")
async def root():
    return {"message": "Nanobot AI Server is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Nanobot AI"}

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        query = data.get("query", "").strip()
        
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if not GROQ_API_KEY:
            raise HTTPException(status_code=500, detail="GROQ API key not configured")

        # For now, using direct query without retriever
        # Once retriever is working, you can add context back
        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful documentation assistant for Flask, FastAPI, and Streamlit. Provide clear, concise answers based on official documentation."
                },
                {"role": "user", "content": query}
            ],
            "temperature": 0.3,
            "max_tokens": 1024
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Groq API error: {response.text}"
            )
            
        response_data = response.json()
        answer = response_data["choices"][0]["message"]["content"]

        return {
            "answer": answer,
            "model": MODEL,
            "tokens_used": response_data.get("usage", {}).get("total_tokens", 0)
        }

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request timeout")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Connection error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Optional: Add endpoint to test retriever once it's ready
# @app.get("/test-retriever")
# async def test_retriever():
#     try:
#         test_query = "What is Flask?"
#         context = retriever.get_relevant_docs(test_query, top_k=3)
#         return {"query": test_query, "context": context}
#     except Exception as e:
#         return {"error": str(e)}