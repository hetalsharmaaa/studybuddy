from fastapi import APIRouter, UploadFile, File, Form
import os
from app.services.pdf_service import extract_text

router = APIRouter()

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    # CASE 1: File exists
    if file:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        extracted_text = extract_text(file_path)

        return {
            "source": "file",
            "filename": file.filename,
            "extracted_preview": extracted_text[:1000],
            "user_query": text if text else None
        }

    # CASE 2: Only text
    if text:
        return {
            "source": "text",
            "content": text[:1000]
        }

    return {"error": "No input provided"}