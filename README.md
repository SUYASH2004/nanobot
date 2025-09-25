# Nanobot

A RAG-based chatbot with Streamlit frontend and Flask backend.

## Project Structure
Nanobot/
├── frontend/
│ ├── app.py # Streamlit application
│ └── req.txt # Frontend dependencies
├── backend/
│ ├── app.py # Flask application
│ ├── requirements.txt # Backend dependencies
│ ├── chunking.py # Text chunking utilities
│ ├── rag.py # RAG implementation
│ ├── scrape_flask_docs.py # Documentation scraper
│ └── .env # Environment variables (add to .gitignore)
└── README.md

text

## Setup Instructions

### Backend
1. Navigate to backend folder
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run: `python app.py`

### Frontend
1. Navigate to frontend folder
2. Install dependencies: `pip install -r req.txt`
3. Run: `streamlit run app.py`
