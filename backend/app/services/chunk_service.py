# backend/app/services/chunk_service.py

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    """
    Larger chunks = fewer chunks = faster embedding.
    1000 chars per chunk instead of 500.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks