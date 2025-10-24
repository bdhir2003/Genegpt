# openai_client.py

import streamlit as st
from openai import OpenAI

# 1. Load key securely from Streamlit Secrets
#    In Streamlit Cloud, you must have:
#    OPENAI_API_KEY="sk-proj-xxxx..."
#    in the Secrets editor.
api_key = st.secrets.get("OPENAI_API_KEY", None)

if not api_key:
    # If we don't have a key at all, raise so app_streamlit catches it
    raise RuntimeError(
        "OPENAI_API_KEY is missing from Streamlit secrets. "
        "Set it in the Streamlit Cloud 'Secrets' panel like:\n"
        'OPENAI_API_KEY="sk-proj-...."'
    )

# 2. Build OpenAI client
client = OpenAI(api_key=api_key)

def simplify_text_for_patient(structured_text: str) -> str:
    """
    Take the structured genetic explanation (answer_text)
    and rewrite it in calm, simple, non-medical-advice language.
    """

    prompt = f"""
You are a genetics explainer for patients.

Rewrite the information below so a non-technical adult can understand it
(about an 8th grade reading level). Keep it calm and factual.
Do NOT give medical advice, do NOT suggest treatment,
do NOT say what will happen in the future.
Remind them to talk to a clinician for personal guidance.

Text to rewrite:
\"\"\"{structured_text}\"\"\"
    """.strip()

    # 3. Call OpenAI
    resp = client.responses.create(
        model="gpt-5-thinking",
        input=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # 4. Extract the text from the response safely
    try:
        simplified = resp.output[0].content[0].text
    except Exception:
        simplified = (
            "I couldn't simplify that right now, but please read the structured explanation above "
            "and talk to a qualified clinician."
        )

    return simplified
