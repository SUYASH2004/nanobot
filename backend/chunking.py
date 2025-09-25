import json
import os

def chunk_text(text, max_length=500):
    """
    Split text into chunks of ~max_length characters.
    """
    chunks = []
    current = ""
    for sentence in text.split(". "):
        if len(current) + len(sentence) <= max_length:
            current += sentence + ". "
        else:
            chunks.append(current.strip())
            current = sentence + ". "
    if current:
        chunks.append(current.strip())
    return chunks

def create_chunks():
    with open("data/flask_docs.json", "r", encoding="utf-8") as f:
        docs = json.load(f)

    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc, max_length=500))

    print(f"✅ Created {len(all_chunks)} chunks.")

    os.makedirs("data", exist_ok=True)
    with open("data/metadata.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    create_chunks()