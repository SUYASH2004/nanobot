import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Fix the import - use relative import
try:
    from .rag import answer_query
except ImportError:
    # Fallback for direct execution
    from rag import answer_query

@app.route('/')
def home():
    return jsonify({"status": "OK", "message": "Flask backend running"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/answer', methods=['POST'])
def api_answer():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({"error": "Question parameter is required"}), 400
            
        answer = answer_query(question)
        return jsonify({"question": question, "answer": answer})
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)