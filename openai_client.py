# openai_client.py
import streamlit as st
from openai import OpenAI

# grab the key from Streamlit Secrets
# (make sure in Streamlit Cloud you added OPENAI_API_KEY="sk-proj-.....")
_api_key = st.secrets["OPENAI_API_KEY"]

# build one client
client = OpenAI(api_key=_api_key)

def simplify_text_for_patient(structured_text: str) -> str:
    """
    Takes the structured 5-part answer (what is it / what is known / not medical advice / etc.)
    and asks the model to rewrite it in calm, simple language for a non-technical person.
    Returns just the simplified text string.
    """

    # You can tune this prompt however you like, but keep it safe and not medical-advice-y.
    prompt = f"""
You are a genetics explainer for patients.
Rewrite the following information in clear 8th-grade English.
Do NOT give medical advice, do NOT tell them what treatment to do,
and remind them to speak to a clinician for any decisions.

Text to rewrite:
\"\"\"{structured_text}\"\"\" 
    """.strip()

    # Call the Responses API
    resp = client.responses.create(
        model="gpt-5-thinking",
        input=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Extract the text part from the response
    try:
        simplified = resp.output[0].content[0].text
    except Exception:
        simplified = "I couldn't summarize that in plain language."

    return simplified
