import argparse

import pandas as pd

from cleaner import clean_dataframe


def build_parser():
    parser = argparse.ArgumentParser(
        description="Clean CSV data and export it to Parquet."
    )
    parser.add_argument("--in", dest="input_file", required=True)
    parser.add_argument("--out", dest="output_file", required=True)
    return parser


def main():
    args = build_parser().parse_args()

    dataframe = pd.read_csv(args.input_file)
    cleaned, report = clean_dataframe(dataframe)

    cleaned.to_parquet(args.output_file, index=False)

    print(f"Rows read: {report['rows_read']}")
    print(f"Duplicates removed: {report['duplicates_removed']}")
    print(f"Missing values: {report['missing_values']}")
    print(
        f"Numeric conversion errors: "
        f"{report['numeric_conversion_errors']}"
    )
    print(f"Rows exported: {report['rows_exported']}")
    print(f"Saved to: {args.output_file}")


if __name__ == "__main__":
    main()
    