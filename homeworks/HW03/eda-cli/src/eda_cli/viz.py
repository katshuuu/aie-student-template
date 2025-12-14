import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def plot_histograms(df: pd.DataFrame, out_dir: Path, max_columns: int = 5):
    numeric_cols = df.select_dtypes(include="number").columns[:max_columns]

    for col in numeric_cols:
        plt.figure()
        df[col].hist(bins=30)
        plt.title(col)
        plt.tight_layout()
        plt.savefig(out_dir / f"hist_{col}.png")
        plt.close()
