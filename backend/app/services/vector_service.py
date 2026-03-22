import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = None
index = None
stored_chunks = []


def get_model():
    global model
    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
        print("Model loaded ✅")
    return model


def store_in_faiss(chunks):
    global index, stored_chunks

    model = get_model()
    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    stored_chunks = chunks


def search(query, k=5):
    global index, stored_chunks

    if index is None:
        return ["No document uploaded"]

    model = get_model()
    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), k)

    return [stored_chunks[i] for i in indices[0] if i < len(stored_chunks)]