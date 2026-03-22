# backend/app/api/chat.py

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.vector_service import search
from app.services.ai_service import generate_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")  # ✅ IMPORTANT
def chat(request: ChatRequest):
    question = request.question

    chunks = search(question)

    answer = generate_answer(chunks, question)

    return {"answer": answer}