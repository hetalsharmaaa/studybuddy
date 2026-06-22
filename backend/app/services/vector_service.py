import os
import numpy as np
import faiss
import httpx

stored_chunks = []
is_ready = False
index = None

HF_TOKEN = os.getenv("HF_TOKEN")
HF_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"

def get_embedding(texts: list[str]) -> np.ndarray:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = httpx.post(
        HF_URL,
        headers=headers,
        json={"inputs": texts, "options": {"wait_for_model": True}},
        timeout=30,
    )
    data = response.json()
    return np.array(data, dtype=np.float32)

def store_in_faiss(chunks: list[str]):
    global stored_chunks, is_ready, index
    stored_chunks = chunks
    embeddings = get_embedding(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    is_ready = True

def search(query: str, top_k: int = 5) -> list[str]:
    if not is_ready or index is None:
        return []
    query_vec = get_embedding([query])
    _, indices = index.search(query_vec, top_k)
    return [stored_chunks[i] for i in indices[0] if i < len(stored_chunks)]

def get_model():
    print("Using HF Inference API for embeddings ✅")