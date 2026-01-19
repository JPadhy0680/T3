
# Key additions only (already included in app_listedness.py)

# --- New uploader in Upload & Parse ---
listedness_file = st.file_uploader(
    "Upload Listedness Excel (columns: Drug Name, LLT)",
    type=["xlsx"],
    help="Pair-list for product × LLT listedness.",
    key=f"listedness_uploader_{ver}"
)

# --- Helper to turn listedness DataFrame into a normalized pair set ---
def to_pair_set(df: pd.DataFrame) -> Set[Tuple[str, str]]:
    pairs: Set[Tuple[str, str]] = set()
    if df is None or df.empty:
        return pairs
    cols = {c.strip().lower(): c for c in df.columns}
    drug_col = cols.get('drug name')
    llt_col = cols.get('llt')
    if not drug_col or not llt_col:
        st.warning("Listedness file must have columns: 'Drug Name' and 'LLT'.")
        return pairs
    for _, row in df[[drug_col, llt_col]].dropna(how='any').iterrows():
        drug = normalize_text(str(row[drug_col]))
        llt = normalize_text(str(row[llt_col]))
        if drug and llt:
            pairs.add((drug, llt))
    return pairs

# --- Read listedness file ---
listedness_pairs: Set[Tuple[str, str]] = set()
if listedness_file:
    ldf = pd.read_excel(listedness_file, engine="openpyxl")
    listedness_pairs = to_pair_set(ldf)

# --- During event parsing: collect LLT terms (normalized) ---
llt_terms_observed: Set[str] = set()
# llt_term = ... (from mapping or value@displayName)
if llt_term:
    llt_terms_observed.add(normalize_text(llt_term))

# --- During product parsing: we already collect Celix suspect products
#     in case_drug_dates_display; we normalize product names
#     when building observed pairs.

# --- Build observed pairs and set Listedness ---
observed_pairs = set()
if listedness_pairs:
    for prod, _, _, _ in case_drug_dates_display:
        if not prod:
            continue
        pnorm = normalize_text(prod)
        for llt in llt_terms_observed:
            observed_pairs.add((pnorm, llt))
    is_listed = any(pair in listedness_pairs for pair in observed_pairs)
else:
    is_listed = False
listedness_val = "Listed" if is_listed else "Unlisted"

# --- Add to output row ---
'Listedness': listedness_val,












