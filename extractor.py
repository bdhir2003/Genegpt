# extractor.py
import re

# Allowed genes for now (controlled scope)
KNOWN_GENES = {"TP53", "PTEN", "EGFR", "BRCA1", "BRCA2"}

# --- Regex helpers ---

# rsID like rs12345
RSID_PATTERN = re.compile(r"\brs\d+\b", re.IGNORECASE)

# protein-style HGVS like p.R175H or p.L858R
HGVS_PROTEIN_PATTERN = re.compile(r"\bp\.[A-Z]\d+[A-Z]\b")

# coding-style HGVS like c.68_69delAG
HGVS_DEL_PATTERN = re.compile(r"\bc\.\d+[_\d]*[A-Z]*del[A-Z]*\b")

# BRCA-style deletions like 185delAG
BRCA_STYLE_DEL_PATTERN = re.compile(r"\b\d+del[A-Z]+\b", re.IGNORECASE)


def extract_gene_and_variant(user_text: str):
    """
    Look at the user's question and pull out:
    - gene (TP53, BRCA1, etc.)
    - variant (e.g. p.R175H, rs12345, 185delAG, c.68_69delAG)
    
    Returns:
        gene (str or None),
        variant (str or None),
        needs_clarification (bool)
    """

    if not user_text:
        return None, None, False

    text_up = user_text.upper().strip()

    # 1. Try to detect which gene they are talking about
    gene = next((g for g in KNOWN_GENES if g in text_up), None)

    # 2. Try to detect which variant they are talking about
    match_rsid = RSID_PATTERN.search(user_text)
    match_hgvs_p = HGVS_PROTEIN_PATTERN.search(user_text)
    match_hgvs_del = HGVS_DEL_PATTERN.search(user_text)
    match_brca_del = BRCA_STYLE_DEL_PATTERN.search(user_text)

    variant = None
    for m in [match_rsid, match_hgvs_p, match_hgvs_del, match_brca_del]:
        if m:
            variant = m.group(0)
            break

    # If we got a gene but no variant, we need to ask the user for the exact variant
    needs_clarification = (gene is not None and variant is None)

    return gene, variant, needs_clarification


def needs_variant_clarification(gene: str, variant: str) -> bool:
    """
    Convenience helper we can call in the UI.
    True = we should ask the user for exact variant code.
    """
    return gene is not None and variant is None


# This makes sure these functions are visible when you do
# `from extractor import extract_gene_and_variant`
__all__ = ["extract_gene_and_variant", "needs_variant_clarification", "KNOWN_GENES"]
