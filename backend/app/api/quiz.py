# backend/app/api/quiz.py

from fastapi import APIRouter
from pydantic import BaseModel
import json

from app.services import vector_service
from app.services.ai_service import get_client

router = APIRouter()


class QuizRequest(BaseModel):
    num_questions: int = 10


@router.post("/quiz")
def generate_quiz(request: QuizRequest):
    chunks = vector_service.stored_chunks

    if not chunks:
        return {"error": "No document uploaded"}

    client = get_client()

    context = "\n\n".join(chunks[:10])

    prompt = f"""You are a strict exam generator.

Generate {request.num_questions} HIGH QUALITY MCQs from the text.

RULES:
- Questions must be factual from text
- No guessing
- No generic questions
- Each must test understanding
- 4 options only
- Only 1 correct answer
- Include explanation

RETURN ONLY VALID JSON:

[
  {{
    "question": "...",
    "options": ["A...", "B...", "C...", "D..."],
    "answer": "A",
    "explanation": "Why this is correct"
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

        quiz = json.loads(output)
        return {"quiz": quiz}

    except Exception as e:
        print("QUIZ ERROR:", e)
        return {"error": "Quiz generation failed"}