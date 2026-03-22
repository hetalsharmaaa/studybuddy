from fastapi import APIRouter, UploadFile, File
import os
import time

from app.services.pdf_service import extract_text
from app.services.chunk_service import chunk_text
from app.services.vector_service import store_in_faiss

router = APIRouter()

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    start_time = time.time()

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    extracted_text = extract_text(file_path)

    chunks = chunk_text(extracted_text)

    store_in_faiss(chunks)

    end_time = time.time()

    return {
        "filename": file.filename,
        "chunks_created": len(chunks),
        "processing_time_seconds": round(end_time - start_time, 2),
    }