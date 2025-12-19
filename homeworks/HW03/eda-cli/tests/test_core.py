import pandas as pd
from eda_cli.core import compute_quality_flags


def test_has_constant_columns():
    df = pd.DataFrame({
        "a": [1, 1, 1],
        "b": [1, 2, 3],
    })

    flags = compute_quality_flags(df)

    assert flags["has_constant_columns"] is True
    assert "a" in flags["constant_columns"]
