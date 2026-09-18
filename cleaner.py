import pandas as pd


NUMERIC_COLUMNS = ("amount", "price", "quantity")


def normalize_columns(df):
    cleaned = df.copy()
    cleaned.columns = [
        column.strip().lower().replace(" ", "_")
        for column in cleaned.columns
    ]
    return cleaned


def remove_duplicates(df):
    return df.drop_duplicates().reset_index(drop=True)


def convert_numeric_columns(df, columns=NUMERIC_COLUMNS):
    cleaned = df.copy()
    conversion_errors = 0

    for column in columns:
        if column in cleaned.columns:
            original = cleaned[column]
            converted = pd.to_numeric(original, errors="coerce")

            conversion_errors += int(
                (original.notna() & converted.isna()).sum()
            )

            cleaned[column] = converted

    return cleaned, conversion_errors


def clean_dataframe(df):
    original_rows = len(df)
    original_missing = int(df.isna().sum().sum())

    cleaned = normalize_columns(df)
    cleaned, conversion_errors = convert_numeric_columns(cleaned)
    cleaned = remove_duplicates(cleaned)

    report = {
        "rows_read": original_rows,
        "duplicates_removed": original_rows - len(cleaned),
        "missing_values": original_missing,
        "numeric_conversion_errors": conversion_errors,
        "rows_exported": len(cleaned),
    }

    return cleaned, report