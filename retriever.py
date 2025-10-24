# retriever.py

import csv
from typing import List, Dict, Optional

def load_seed_dataset(path: str = "data/genegpt_seed_dataset.csv") -> List[Dict[str, str]]:
    """
    Load the CSV with our known gene/variant records.
    Returns a list of dicts (each dict is one row).
    """
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def find_variant_record(
    rows: List[Dict[str, str]],
    gene: str,
    variant: str
) -> Optional[Dict[str, str]]:
    """
    Find the row in our dataset that matches this gene + variant.

    Matching rules:
    - 'gene' column must match the extracted gene.
    - The user-supplied variant must match EITHER:
        - variant_hgvs (like p.R175H, 185delAG)
        - OR dbsnp_rsid (like rs28934578)

    If we find exactly one match, return that row dict.
    Otherwise return None.
    """

    if not gene:
        return None

    gene_up = gene.upper()
    variant_low = variant.lower() if variant else None

    candidates = []

    for r in rows:
        row_gene = r.get("gene", "").upper()
        row_hgvs = r.get("variant_hgvs", "").lower()
        row_rsid = r.get("dbsnp_rsid", "").lower()

        if row_gene == gene_up:
            if variant_low and (variant_low == row_hgvs or variant_low == row_rsid):
                candidates.append(r)

    if len(candidates) == 1:
        return candidates[0]

    # 0 matches or >1 matches → we refuse to guess
    return None
