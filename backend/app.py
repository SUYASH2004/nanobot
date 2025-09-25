import os
from flask import Flask, jsonify, request
from flask_cors import CORS  # Add this import
from backend.rag import answer_query  # Fix import

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

@app.route('/')
def home():
    return jsonify({"message": "Flask API is running"})

@app.route('/api/answer', methods=['POST'])
def get_answer():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
            
        answer = answer_query(question)
        return jsonify({"answer": answer})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Production configuration
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)