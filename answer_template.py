# answer_template.py

EDUCATION_DISCLAIMER = (
    "This information is for education only and is not medical advice. "
    "Please talk to a qualified clinician or genetic counselor about your personal results."
)

def build_answer(record: dict, gene: str, variant: str) -> str:
    """
    Turn a record from our dataset into a safe, 5-part explanation.
    """
    gene_name = record.get("gene", gene)
    function_note = record.get("function_note", "")
    classification = record.get("classification", "Reported in studies.")
    condition = record.get("condition", "No condition available.")
    clinvar_url = record.get("clinvar_url", "N/A")
    dbsnp_url = record.get("dbsnp_url", "N/A")
    ncbi_gene_url = record.get("ncbi_gene_url", "N/A")

    # 1. What is it?
    part1 = f"{gene_name} is a gene. {function_note} {variant} is a change (variant) in this gene."

    # 2. What is known?
    part2 = f"This variant has been {classification} and is associated with {condition}."

    # 3. What this does NOT mean
    part3 = "This does not diagnose you or predict what will happen to you."

    # 4. What to do next
    part4 = "Please discuss this result with a clinician or genetic counselor."

    # 5. Trusted sources
    part5 = (
        "Trusted sources:\n"
        f"- ClinVar: {clinvar_url}\n"
        f"- dbSNP: {dbsnp_url}\n"
        f"- NCBI Gene: {ncbi_gene_url}"
    )

    return (
        f"1. What is it?\n{part1}\n\n"
        f"2. What is known?\n{part2}\n\n"
        f"3. What this does NOT mean\n{part3}\n\n"
        f"4. What to do next\n{part4}\n\n"
        f"5. Trusted sources\n{part5}\n\n"
        f"{EDUCATION_DISCLAIMER}"
    )
