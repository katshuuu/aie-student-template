import json
import click
import pandas as pd
from pathlib import Path

from eda_cli.core import compute_quality_flags
from eda_cli.viz import plot_histograms


@click.group()
def cli():
    pass


@cli.command()
@click.argument("csv_path")
def overview(csv_path):
    df = pd.read_csv(csv_path)
    flags = compute_quality_flags(df)
    click.echo(flags)


@cli.command()
@click.argument("csv_path")
@click.option("--out-dir", required=True, help="Output directory")
@click.option("--max-hist-columns", default=5, show_default=True)
@click.option("--title", default="EDA Report", show_default=True)
@click.option("--min-missing-share", default=0.1, show_default=True)
@click.option("--json-summary", is_flag=True, help="Save JSON summary")
def report(csv_path, out_dir, max_hist_columns, title, min_missing_share, json_summary):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    flags = compute_quality_flags(df)

    plot_histograms(df, out_dir, max_columns=max_hist_columns)

    report_md = out_dir / "report.md"
    with report_md.open("w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("## Dataset shape\n")
        f.write(f"- Rows: {flags['n_rows']}\n")
        f.write(f"- Columns: {flags['n_cols']}\n\n")

        f.write("## Quality\n")
        f.write(f"- Quality score: {flags['quality_score']}\n")
        f.write(f"- Constant columns: {flags['constant_columns']}\n")
        f.write(f"- High cardinality columns: {flags['high_cardinality_columns']}\n\n")

        f.write(f"Missing threshold: {min_missing_share}\n")

    if json_summary:
        summary = {
            "n_rows": flags["n_rows"],
            "n_cols": flags["n_cols"],
            "quality_score": flags["quality_score"],
            "problematic_columns": {
                "constant": flags["constant_columns"],
                "high_cardinality": flags["high_cardinality_columns"],
            },
        }
        with (out_dir / "summary.json").open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
