🤖 Nanobot

A Retrieval-Augmented Generation (RAG) based chatbot built with Flask (backend) and Streamlit (frontend).
Nanobot scrapes the Flask official documentation, chunks it, builds embeddings with FAISS, and lets you query docs conversationally.

📂 Project Structure
Nanobot/
├── frontend/
│   ├── app.py              # Streamlit application (UI)
│   └── req.txt             # Frontend dependencies
│
├── backend/
│   ├── app.py              # Flask application (API server)
│   ├── requirements.txt    # Backend dependencies
│   ├── chunking.py         # Text chunking utilities
│   ├── rag.py              # RAG implementation (retrieval + LLM call)
│   ├── scrape_flask_docs.py# Documentation scraper
│   ├── embeddings.py       # FAISS index builder
│   └── .env                # Environment variables (add to .gitignore)
│
└── README.md               # Project guide

⚙️ Setup Instructions
🔹 Backend

Navigate to the backend folder:

cd backend


Install dependencies:

pip install -r requirements.txt


Create a .env file and add your API key (Groq / DeepSeek / Gemini etc.):

GROQ_API_KEY=your_api_key_here


Scrape Flask docs and build embeddings:

python scrape_flask_docs.py
python chunking.py
python embeddings.py


Start the Flask server:

python app.py

🔹 Frontend

Navigate to the frontend folder:

cd frontend


Install dependencies:

pip install -r req.txt


Run the Streamlit app:

streamlit run app.py

🚀 Usage

Open the Streamlit frontend (URL will be shown in terminal, usually http://localhost:8501
).

Type your question (e.g., “Flask mein GET aur POST request kaise handle karte hain?”).

Nanobot will:

Retrieve relevant chunks from the Flask docs.

Pass them to the LLM (via API).

Return a concise, contextual answer.

🛠️ Tech Stack

Backend: Flask, FAISS, Python

Frontend: Streamlit, Tailwind CSS (via custom styling)

RAG: Custom retriever + FAISS index

LLM APIs: Groq / DeepSeek / Gemini (configurable)

