from flask import Flask, request, jsonify
from flask_cors import CORS
from rag import answer_query

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/api/ask", methods=["GET", "POST"])
def ask():
    print("📥 Received request to /api/ask")
    print(f"📥 Method: {request.method}")
    
    # Handle both GET and POST
    if request.method == "GET":
        question = request.args.get("question", "") or request.args.get("q", "")
        print(f"📥 GET question: {question}")
    else:
        data = request.get_json()
        print(f"📥 POST data: {data}")
        question = data.get("question", "") if data else ""
    
    if not question:
        return jsonify({"error": "Missing question", "success": False}), 400

    try:
        print(f"🤔 Processing question: {question}")
        answer = answer_query(question)
        print(f"✅ Answer generated: {answer[:100]}...")
        
        return jsonify({
            "question": question, 
            "answer": answer,
            "success": True
        })
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@app.route("/api/courses", methods=["GET"])
def get_courses():
    courses = [
        {
            "id": "flask",
            "name": "Flask Documentation",
            "description": "Learn Flask web framework",
            "status": "active"
        }
    ]
    return jsonify(courses)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Backend is running!"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "LearnBot Academy Backend API",
        "endpoints": {
            "health": "/health",
            "courses": "/api/courses", 
            "ask": "/api/ask"
        }
    })

if __name__ == "__main__":
    print("🚀 Starting Flask server on http://127.0.0.1:8000")
    print("📋 Available endpoints:")
    print("   - GET  /health")
    print("   - GET  /api/courses") 
    print("   - GET/POST /api/ask")
    app.run(debug=True, port=8000, host='127.0.0.1')