import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

class DocRetriever:
    def __init__(self, data_folder=None):
        try:
            # Get the absolute path to the data folder
            if data_folder is None:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                data_folder = os.path.join(current_dir, "..", "..", "data")
            
            data_folder = os.path.abspath(data_folder)
            print(f"Looking for data in: {data_folder}")
            
            # Create data folder if it doesn't exist
            os.makedirs(data_folder, exist_ok=True)
            
            # Check if index already exists
            index_path = os.path.join(data_folder, "docs_index.faiss")
            sentences_path = os.path.join(data_folder, "sentences.pkl")
            
            if os.path.exists(index_path) and os.path.exists(sentences_path):
                print("Loading existing index...")
                self.load_index(data_folder)
            else:
                print("Creating new index...")
                self._create_new_index(data_folder)
                
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            print("DocRetriever initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing DocRetriever: {e}")
            raise

    def _create_new_index(self, data_folder):
        """Create a new FAISS index from documents"""
        self.sentences = []
        files = ["flask_docs.txt", "fastapi_docs.txt", "streamlit_docs.txt"]

        for file in files:
            file_path = os.path.join(data_folder, file)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    paragraphs = f.read().split("\n\n")
                    self.sentences.extend([p for p in paragraphs if p.strip()])
                print(f"Loaded {file}")
            else:
                print(f"Warning: {file} not found, creating sample...")
                self._create_sample_file(file_path, file)

        if not self.sentences:
            raise ValueError("No documents found to create index")

        # Create embeddings
        self.embeddings = self.model.encode(self.sentences, convert_to_numpy=True)
        self.dimension = self.embeddings.shape[1]

        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(self.embeddings)

        # Save for later use
        faiss.write_index(self.index, os.path.join(data_folder, "docs_index.faiss"))
        with open(os.path.join(data_folder, "sentences.pkl"), "wb") as f:
            pickle.dump(self.sentences, f)
        
        print(f"Created index with {len(self.sentences)} sentences")

    def _create_sample_file(self, file_path, filename):
        """Create sample documentation files"""
        sample_content = {
            "flask_docs.txt": """Flask is a micro web framework written in Python.

It is classified as a microframework because it does not require particular tools or libraries.

Flask has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions.

However, Flask supports extensions that can add application features as if they were implemented in Flask itself.""",

            "fastapi_docs.txt": """FastAPI is a modern, fast web framework for building APIs with Python 3.6+ based on standard Python type hints.

FastAPI is built on top of Starlette for web parts and Pydantic for data parts.

It has excellent performance, on par with NodeJS and Go thanks to Starlette and Pydantic.""",

            "streamlit_docs.txt": """Streamlit is an open-source app framework for Machine Learning and data science teams.

Streamlit turns data scripts into shareable web apps in minutes.

All in pure Python. No front-end experience required."""
        }
        
        content = sample_content.get(filename, f"Sample content for {filename}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created sample file: {file_path}")

    def load_index(self, data_folder):
        """Load existing FAISS index"""
        self.index = faiss.read_index(os.path.join(data_folder, "docs_index.faiss"))
        with open(os.path.join(data_folder, "sentences.pkl"), "rb") as f:
            self.sentences = pickle.load(f)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print(f"Loaded index with {len(self.sentences)} sentences")

    def get_relevant_docs(self, query, top_k=5):
        """Retrieve relevant documents for a query"""
        try:
            query_emb = self.model.encode([query], convert_to_numpy=True)
            distances, indices = self.index.search(query_emb, top_k)
            relevant_docs = [self.sentences[i] for i in indices[0] if i < len(self.sentences)]
            return "\n\n".join(relevant_docs)
        except Exception as e:
            print(f"Error in get_relevant_docs: {e}")
            return "No relevant documents found."