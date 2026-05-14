import pandas as pd

COLUMNS_NAME = ["time", "x", "y", "z", "abs"]


def load_data(path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = COLUMNS_NAME
    return df

