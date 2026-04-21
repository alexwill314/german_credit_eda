import numpy as np
import pandas as pd
import re


def parse_codetable(code_table: str) -> pd.DataFrame:
    """
        Parses a semi-structured codebook into a structured DataFrame.

        Returns columns:
        - column_old
        - column_new
        - code
        - label
        """
    with open(code_table, "r", encoding="utf-8") as f:
        lines = f.readlines()

    rows = []
    current_old = None
    current_new = None
    has_codes = False

    def flush_current():
        """adds dummy line when variable has no codes"""
        if current_old is not None and not has_codes:
            rows.append({
                "column_old": current_old,
                "column_new": current_new,
                "code": np.nan,
                "label": np.nan
            })

    for line in lines:
        line = line.strip()

        # recognise new variable
        if line.startswith("$"):
            flush_current()

            #set new variable
            var_match = re.match(r"\$`(.+?) = (.+?)`", line)
            if var_match:
                current_old = var_match.group(1)
                current_new = var_match.group(2)
                has_codes = False

        # recognise codes
        elif re.match(r"\d+\s*:", line):
            code, label = line.split(":", 1)
            rows.append({
                "column_old": current_old,
                "column_new": current_new,
                "code": int(code.strip()),
                "label": label.strip()
            })
            has_codes = True

    #flush so last variable is not left over
    flush_current()

    code_df = pd.DataFrame(rows)
    return code_df


def rename_columns(df: pd.DataFrame, code_df: pd.DataFrame) -> pd.DataFrame:
    """rename columns according to code table"""
    rename_map = (
        code_df.drop_duplicates("column_old").set_index("column_old")["column_new"].to_dict())

    df = df.rename(columns=rename_map)
    return df

def map_codes(df: pd.DataFrame, code_df: pd.DataFrame) -> pd.DataFrame:
    """map codes according to code table"""
    cat_df = code_df.dropna(subset=["code"])

    for col in cat_df["column_new"].unique():
        mapping = (
            cat_df[cat_df["column_new"] == col].set_index("code")["label"].to_dict())

        if col in df.columns:
            df[col] = df[col].map(mapping).fillna(df[col])
    return df

def clean_categorical(df: pd.DataFrame, code_df: pd.DataFrame) -> pd.DataFrame:
    """categorical cleaning"""
    cat_df = code_df.dropna(subset=["code"])

    for col in df.select_dtypes(include="object").columns:
        df[col] = pd.Categorical(df[col],
                                 categories = cat_df.loc[cat_df["column_new"] == col, "label"],
                                 ordered = True)
    return df


def prepare_data(df: pd.DataFrame, code_table: str) -> pd.DataFrame:
    """data preparation pipeline"""
    code_df = parse_codetable(code_table)
    df = rename_columns(df,code_df)
    df = map_codes(df,code_df)
    df = clean_categorical(df, code_df)
    return df