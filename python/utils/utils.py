import os
import pandas as pd

def get_csv_data(file, index_col=None, **kwargs):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "..", "data", f"{file}.csv")
    return pd.read_csv(file_path, index_col=index_col, **kwargs)

def save_csv_data(df,filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "..", "data", f"{filename}.csv")
    df.to_csv(file_path)