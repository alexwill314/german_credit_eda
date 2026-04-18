import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """Load dataset from CSV."""
    return pd.read_csv(path, index_col=0)


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names (adapt if needed)."""
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    return df


def clean_categorical(df: pd.DataFrame) -> pd.DataFrame:
    """Basic categorical cleaning."""
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.lower().str.strip()
    return df


def prepare_data(path: str) -> pd.DataFrame:
    """Full data preparation pipeline."""
    df = load_data(path)
    df = rename_columns(df)
    df = clean_categorical(df)
    return df