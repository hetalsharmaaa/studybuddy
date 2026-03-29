# backend/app/services/ai_service.py

from groq import Groq
import os


def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


MODE_PROMPTS = {
    "teacher": "You are an experienced professor. Explain in depth with examples, analogies, and structured points. Use headings if needed.",
    "simple": "You are explaining to a 10-year-old. Use very simple words, short sentences, and fun examples. Avoid jargon completely.",
    "exam": "You are an exam coach. Give a concise, exam-ready answer. Use bullet points. Highlight key terms. Be precise and to the point.",
    "revision": "You are a quick revision assistant. Summarize the answer in 3-5 bullet points only. Be extremely brief and clear.",
    "default": "You are a helpful AI tutor. Answer clearly and helpfully.",
}


def generate_answer(context_chunks, question, mode="default"):
    client = get_client()

    mode_instruction = MODE_PROMPTS.get(mode, MODE_PROMPTS["default"])

    if not context_chunks or (len(context_chunks) > 0 and "No document" in context_chunks[0]):
        prompt = f"""{mode_instruction}

Answer this question:
{question}
"""
    else:
        context = "\n\n".join(context_chunks[:3])

        prompt = f"""{mode_instruction}

Use ONLY the context below to answer the question.

CONTEXT:
{context}

QUESTION:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content