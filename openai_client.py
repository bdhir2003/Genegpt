# openai_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the OpenAI client using the key in .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY=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"))

def simplify_text_for_patient(full_answer_text: str) -> str:
    """
    Take the structured, factual answer (the 5-part output),
    and rewrite it in gentle, clear, 8th-grade-level English.
    We DO NOT want diagnosis, and we DO want safety language.
    """

    prompt = f"""
You are a careful medical explainer. Rewrite the text below in simple, friendly language
for a non-medical person. Keep it short. Do not add any medical promises, do not guess,
do not say they have a disease. Remind them to talk to a clinician.

Text to rewrite:
\"\"\" 
{full_answer_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.3,  # keep it steady, not creative
        messages=[
            {"role": "system",
             "content": "You are a genetics helper. You speak calmly, clearly, and safely. You never diagnose."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
