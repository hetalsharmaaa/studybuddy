import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
print("Model loaded ✅")

index = None
stored_chunks = []


def create_embeddings(chunks):
    return model.encode(chunks)


def store_in_faiss(chunks):
    global index, stored_chunks

    if not chunks:
        return

    embeddings = create_embeddings(chunks)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    stored_chunks = chunks


def search(query, k=5):   # 🔥 increased from 3 → 5
    global index, stored_chunks

    if index is None:
        return ["No document uploaded yet."]

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    results = []

    for i in indices[0]:
        if i < len(stored_chunks):
            chunk = stored_chunks[i]

            # 🔥 remove very small / useless chunks
            if len(chunk.strip()) > 50:
                results.append(chunk)

    return results