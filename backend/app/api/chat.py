from fastapi import APIRouter
from pydantic import BaseModel
from app.services.vector_service import search
from app.services.ai_service import generate_answer

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: QueryRequest):
    question = request.question

    chunks = search(question)

    if not chunks or "No document uploaded" in chunks[0]:
        return {"error": "Upload a document first"}

    answer = generate_answer(chunks, question)

    return {
        "question": question,
        "answer": answer,
        "context_used": chunks
    }