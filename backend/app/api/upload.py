from fastapi import APIRouter, UploadFile, File, Form
import os
import time

from app.services.pdf_service import extract_text
from app.services.chunk_service import chunk_text
from app.services.vector_service import store_in_faiss

router = APIRouter()

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

MAX_CHARS = 20000   # limit text size
MAX_CHUNKS = 20     # limit number of chunks


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    start_time = time.time()

    # 📄 CASE 1: File upload
    if file:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 🔍 Extract text
        extracted_text = extract_text(file_path)

        # ⚡ Limit large files
        if len(extracted_text) > MAX_CHARS:
            extracted_text = extracted_text[:MAX_CHARS]

        # ✂️ Chunking
        chunks = chunk_text(extracted_text)

        # ⚡ Limit chunks
        chunks = chunks[:MAX_CHUNKS]

        # 🧠 Store in FAISS
        store_in_faiss(chunks)

        processing_time = round(time.time() - start_time, 2)

        return {
            "source": "file",
            "filename": file.filename,
            "chunks_created": len(chunks),
            "processing_time_seconds": processing_time,
            "preview": chunks[:2]
        }

    # 📝 CASE 2: Text input
    if text:
        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS]

        chunks = chunk_text(text)
        chunks = chunks[:MAX_CHUNKS]

        store_in_faiss(chunks)

        processing_time = round(time.time() - start_time, 2)

        return {
            "source": "text",
            "chunks_created": len(chunks),
            "processing_time_seconds": processing_time,
            "preview": chunks[:2]
        }

    return {"error": "No input provided"}