import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from cleaner import (
    clean_dataframe,
    convert_numeric_columns,
    normalize_columns,
    remove_duplicates,
)


PROJECT = Path(__file__).resolve().parents[1]


class CleanerTests(unittest.TestCase):
    def test_normalize_columns(self):
        df = pd.DataFrame(columns=[" Product Name ", "Unit Price"])

        result = normalize_columns(df)

        self.assertEqual(
            list(result.columns),
            ["product_name", "unit_price"],
        )

    def test_remove_duplicates(self):
        df = pd.DataFrame(
            {
                "id": [1, 1, 2],
                "name": ["A", "A", "B"],
            }
        )

        result = remove_duplicates(df)

        self.assertEqual(len(result), 2)

    def test_numeric_columns_are_converted(self):
        df = pd.DataFrame(
            {
                "amount": ["10", "20"],
                "price": ["2.5", "invalid"],
            }
        )

        result, errors = convert_numeric_columns(df)

        self.assertEqual(result.loc[0, "amount"], 10)
        self.assertEqual(result.loc[0, "price"], 2.5)
        self.assertTrue(pd.isna(result.loc[1, "price"]))
        self.assertEqual(errors, 1)

    def test_missing_numeric_column_is_ignored(self):
        df = pd.DataFrame({"name": ["A"]})

        result, errors = convert_numeric_columns(df)

        self.assertEqual(list(result.columns), ["name"])
        self.assertEqual(errors, 0)

    def test_clean_dataframe_returns_report(self):
        df = pd.DataFrame(
            {
                " Amount ": ["10", "10", "invalid"],
                "Product": ["A", "A", "B"],
            }
        )

        cleaned, report = clean_dataframe(df)

        self.assertEqual(report["rows_read"], 3)
        self.assertEqual(report["duplicates_removed"], 1)
        self.assertEqual(report["rows_exported"], 2)
        self.assertEqual(report["missing_values"], 0)
        self.assertEqual(report["numeric_conversion_errors"], 1)
        self.assertEqual(
            list(cleaned.columns),
            ["amount", "product"],
        )

    def test_numeric_normalization_happens_before_deduplication(self):
        df = pd.DataFrame(
            {
                "amount": ["10", "10.0"],
                "product": ["A", "A"],
            }
        )

        cleaned, report = clean_dataframe(df)

        self.assertEqual(len(cleaned), 1)
        self.assertEqual(report["duplicates_removed"], 1)

    def test_cli_creates_parquet_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            input_file = temp / "raw.csv"
            output_file = temp / "cleaned.parquet"

            input_file.write_text(
                "Product,Amount,Price\n"
                "A,10,2.5\n"
                "A,10,2.5\n"
                "B,invalid,4.0\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(PROJECT / "app.py"),
                    "--in",
                    str(input_file),
                    "--out",
                    str(output_file),
                ],
                capture_output=True,
                text=True,
                cwd=PROJECT,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output_file.exists())
            self.assertIn("Rows exported: 2", result.stdout)
            self.assertIn(
                "Numeric conversion errors: 1",
                result.stdout,
            )


if __name__ == "__main__":
    unittest.main()