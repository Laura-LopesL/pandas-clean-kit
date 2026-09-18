import unittest

import pandas as pd

from cleaner import (
    clean_dataframe,
    convert_numeric_columns,
    normalize_columns,
    remove_duplicates,
)


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

        result = convert_numeric_columns(df)

        self.assertEqual(result.loc[0, "amount"], 10)
        self.assertEqual(result.loc[0, "price"], 2.5)
        self.assertTrue(pd.isna(result.loc[1, "price"]))

    def test_missing_numeric_column_is_ignored(self):
        df = pd.DataFrame({"name": ["A"]})

        result = convert_numeric_columns(df)

        self.assertEqual(list(result.columns), ["name"])

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
        self.assertEqual(report["missing_values"], 1)
        self.assertEqual(
            list(cleaned.columns),
            ["amount", "product"],
        )


if __name__ == "__main__":
    unittest.main()
    