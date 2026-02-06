import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")


def generate_answer(context, question):

    prompt = f"""
You are an Enterprise PDF Assistant.

Use ONLY this context:

{context}

Question: {question}

Answer clearly:
"""

    response = model.generate_content(prompt)
    return response.text
