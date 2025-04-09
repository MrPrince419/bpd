import pandas as pd

def get_filtered_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with missing values."""
    df = df.copy()
    df.dropna(inplace=True)
    return df

def is_valid_dataset(df: pd.DataFrame) -> bool:
    """Check if uploaded data has the required structure."""
    return not df.empty and df.select_dtypes(include=["number", "datetime", "object"]).shape[1] >= 2
