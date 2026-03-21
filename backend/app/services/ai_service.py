from groq import Groq
import os


def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(context_chunks, question):
    client = get_client()

    # 🔥 Clean + limit context
    context = "\n\n".join(context_chunks[:3])  # only top 3 chunks

    prompt = f"""
You are a strict question-answering system.

RULES:
- Answer ONLY from the given context
- If the answer is clearly present → give exact answer
- If not found → say "Answer not found in document"
- DO NOT guess
- DO NOT add extra information

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2   # 🔥 reduces randomness
    )

    return response.choices[0].message.content