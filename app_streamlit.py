# app_streamlit.py
import streamlit as st
from extractor import extract_gene_and_variant
from retriever import load_seed_dataset, find_variant_record
from answer_template import build_answer, EDUCATION_DISCLAIMER

# --- Page config / styling ---
st.set_page_config(
    page_title="GeneGPT (Testing Agent)",
    page_icon="🧬",
    layout="centered"
)

st.markdown(
    """
    <style>
    body {
        background-color: #0f1117;
        color: #f1f5f9;
        font-family: -apple-system,BlinkMacSystemFont,system-ui,"Segoe UI",Roboto,"Helvetica Neue",Arial;
    }
    .response-card {
        border-radius: 1rem;
        padding: 1.2rem 1.4rem;
        background-color: #1e1e1e10;
        border: 1px solid #9993;
        font-size: 0.95rem;
        line-height: 1.45rem;
        white-space: pre-wrap;
        color: #f8fafc;
    }
    .disclaimer {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 0.5rem;
    }
    .user-bubble {
        background: #1e3a8a33;
        border: 1px solid #2563eb55;
        padding: .75rem 1rem;
        border-radius: .75rem;
        margin-bottom: 1rem;
        font-size: .9rem;
        color: #f8fafc;
    }
    .summary-card {
        border-radius: 0.75rem;
        padding: 1rem 1.2rem;
        background-color: #1e293b;
        border: 1px solid #475569;
        font-size: 0.95rem;
        line-height: 1.45rem;
        color: #f8fafc;
        white-space: pre-wrap;
    }
    .summary-header {
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        color: #93c5fd;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar info ---
with st.sidebar:
    st.title("🧬 GeneGPT (Testing)")
    st.write("Goal: explain genetic variants in simple, safe language using trusted data.")
    st.write("Scope right now:")
    st.markdown("- TP53\n- PTEN\n- EGFR\n- BRCA1\n- BRCA2")
    st.caption("This early version only uses a small, manual dataset. No live medical advice.")

st.title("GeneGPT – Variant Explanation Agent (Test Build)")

st.write("Ask about a gene + variant. Example: `I have TP53 p.R175H` or `My report says BRCA1 185delAG`.")

user_question = st.text_input("Your question:")

if st.button("Explain variant"):
    if not user_question.strip():
        st.warning("Please type a question first.")
    else:
        # 1. Extract gene + variant
        gene, variant, needs_clarification = extract_gene_and_variant(user_question)

        st.markdown(
            f"<div class='user-bubble'><b>You asked:</b><br>{user_question}</div>",
            unsafe_allow_html=True
        )

        # --- Case 1: we couldn't find a supported gene
        if gene is None:
            st.error(
                "I could not detect a known gene (TP53, PTEN, EGFR, BRCA1, BRCA2) in your question."
            )

        # --- Case 2: we have gene but we don't have the exact variant
        elif needs_clarification:
            st.info(
                "I found the gene "
                f"`{gene}`, but I could not find the exact variant.\n\n"
                "Please tell me the exact variant code (for example an rsID like `rs12345` "
                "or an HGVS name like `p.R175H`)."
            )

        # --- Case 3: we have gene and variant, try to look it up
        else:
            rows = load_seed_dataset()
            rec = find_variant_record(rows, gene, variant)

            # If it's not in our dataset, we stop safely
            if rec is None:
                st.error(
                    "I recognized your gene and variant format, but that exact pair "
                    "is not in my dataset yet. This system is still in testing."
                )
                st.caption(EDUCATION_DISCLAIMER)

            else:
                # Build the factual, trust-aware answer from our dataset only
                answer_text = build_answer(rec, gene, variant)

                # Show the structured 5-part answer (clinical style)
                st.markdown("<div class='response-card'>", unsafe_allow_html=True)
                st.text(answer_text)
                st.markdown("</div>", unsafe_allow_html=True)

                # Now: plain-language summary from GPT-3.5-turbo
                # We wrap this in try/except so your app never crashes if API fails.
                try:
                    from openai_client import simplify_text_for_patient
                    simple_summary = simplify_text_for_patient(answer_text)

                    st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
                    st.markdown(
                        "<div class='summary-header'>Plain language summary (AI-generated):</div>",
                        unsafe_allow_html=True
                    )
                    st.write(simple_summary)
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.caption(
                        "This summary was generated to make the language easier to understand. "
                        "It is only for education, not medical advice."
                    )

                except Exception as e:
                    # If GPT call fails (no key, offline, etc.), we don't die.
                    st.warning(
                        "I could not generate a plain-language summary right now. "
                        "Please use the structured explanation above."
                    )
                    # You can uncomment this line while debugging, then comment it again:
                    # st.text(f"(Debug info: {e})")
