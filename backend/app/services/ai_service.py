from groq import Groq
import os


def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(context_chunks, question):
    client = get_client()

    # ✅ If no document → normal AI
    if not context_chunks or "No document" in context_chunks[0]:
        prompt = f"""
You are a helpful AI tutor.

Answer clearly:

{question}
"""
    else:
        context = "\n\n".join(context_chunks[:3])

        prompt = f"""
Answer ONLY using this context:

{context}

Question: {question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content