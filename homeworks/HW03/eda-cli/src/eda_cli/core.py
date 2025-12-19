import pandas as pd


def compute_quality_flags(df: pd.DataFrame) -> dict:
    n_rows, n_cols = df.shape

    missing_share = df.isna().mean()
    has_missing = (missing_share > 0).any()
    constant_columns = [
        col for col in df.columns
        if df[col].nunique(dropna=False) <= 1
    ]
    has_constant_columns = len(constant_columns) > 0
    high_cardinality_threshold = max(20, int(0.5 * n_rows))
    high_cardinality_cols = [
        col for col in df.select_dtypes(include="object").columns
        if df[col].nunique() > high_cardinality_threshold
    ]
    has_high_cardinality_categoricals = len(high_cardinality_cols) > 0

    quality_score = 1.0
    if has_missing:
        quality_score -= 0.2
    if has_constant_columns:
        quality_score -= 0.2
    if has_high_cardinality_categoricals:
        quality_score -= 0.2

    return {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "has_missing": has_missing,
        "missing_share": missing_share.to_dict(),
        "has_constant_columns": has_constant_columns,
        "constant_columns": constant_columns,
        "has_high_cardinality_categoricals": has_high_cardinality_categoricals,
        "high_cardinality_columns": high_cardinality_cols,
        "quality_score": round(max(quality_score, 0.0), 2),
    }
