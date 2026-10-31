import argparse
import json
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "Index",
    "Telugu Text",
    "English Text",
    "English Clitic Word",
    "Clitic",
    "swaroopa",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export only swaroopa=yes rows from the Excel workbook to the app's JSON data file."
    )
    parser.add_argument("workbook", type=Path, help="Path to the source .xlsx workbook")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "data" / "sentences.json",
        help="Output JSON path (defaults to data/sentences.json)",
    )
    args = parser.parse_args()

    dataframe = pd.read_excel(args.workbook, engine="openpyxl")
    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        raise ValueError(f"Workbook is missing required columns: {', '.join(sorted(missing_columns))}")

    included = dataframe[
        dataframe["swaroopa"].astype("string").str.strip().str.casefold().eq("yes")
    ]
    sentences = []
    for _, row in included.iterrows():
        sentences.append(
            {
                "Index": int(row["Index"]),
                "English Sentence": "" if pd.isna(row["English Text"]) else str(row["English Text"]),
                "Telugu Sentence": "" if pd.isna(row["Telugu Text"]) else str(row["Telugu Text"]),
                "English Clitic Word": ""
                if pd.isna(row["English Clitic Word"])
                else str(row["English Clitic Word"]),
                "Clitic": "" if pd.isna(row["Clitic"]) else str(row["Clitic"]),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(sentences, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(sentences)} swaroopa=yes sentences to {args.output}")


if __name__ == "__main__":
    main()