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

    for column in columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(
                cleaned[column],
                errors="coerce",
            )

    return cleaned


def clean_dataframe(df):
    original_rows = len(df)

    cleaned = normalize_columns(df)
    cleaned = remove_duplicates(cleaned)
    cleaned = convert_numeric_columns(cleaned)

    report = {
        "rows_read": original_rows,
        "duplicates_removed": original_rows - len(cleaned),
        "missing_values": int(cleaned.isna().sum().sum()),
        "rows_exported": len(cleaned),
    }

    return cleaned, report
