# backend/app/api/questions.py

from fastapi import APIRouter
from pydantic import BaseModel
import json

from app.services import vector_service
from app.services.ai_service import get_client

router = APIRouter()


class QuestionRequest(BaseModel):
    num_questions: int = 5
    question_type: str = "mcq"


@router.post("/questions")
def generate_questions(request: QuestionRequest):
    chunks = vector_service.stored_chunks

    if not chunks:
        return {"error": "No document uploaded yet"}

    client = get_client()

    context = "\n\n".join(chunks[:8])

    if request.question_type == "mcq":
        prompt = f"""You are an expert exam question generator.

Generate {request.num_questions} MCQ questions from the text below.

RETURN ONLY VALID JSON — no extra text, no markdown:

[
  {{
    "question": "...",
    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
    "answer": "A",
    "explanation": "..."
  }}
]

TEXT:
{context}
"""
    else:
        prompt = f"""You are an expert exam question generator.

Generate {request.num_questions} short answer questions from the text below.

RETURN ONLY VALID JSON — no extra text, no markdown:

[
  {{
    "question": "...",
    "answer": "..."
  }}
]

TEXT:
{context}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        output = response.choices[0].message.content.strip()

        if "```" in output:
            output = output.split("```")[1]
            if output.startswith("json"):
                output = output[4:]

        questions = json.loads(output)
        return {"questions": questions, "type": request.question_type}

    except Exception as e:
        print("QUESTION GEN ERROR:", e)
        return {"error": "Question generation failed"}