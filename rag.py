# rag_store.py
import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
INDEX_FILE = "rag_index.faiss"
DATA_FILE = "rag_data.pkl"

dimension = 384
if os.path.exists(INDEX_FILE):
    index = faiss.read_index(INDEX_FILE)
else:
    index = faiss.IndexFlatL2(dimension)

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        data_store = pickle.load(f)
else:
    data_store = []

def add_context(text):
    embedding = EMBED_MODEL.encode([text])
    index.add(embedding)
    data_store.append(text)
    faiss.write_index(index, INDEX_FILE)
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data_store, f)

def retrieve_context(query, k=3):
    if len(data_store) == 0:
        return []
    embedding = EMBED_MODEL.encode([query])
    D, I = index.search(embedding, k)
    return [data_store[i] for i in I[0]]

def delete_context():
    os.remove(INDEX_FILE)
    os.remove(DATA_FILE)