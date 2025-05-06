import importlib
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

def load_dict_file(file_name, attr_name=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "..", "data", f"{file_name}.py")
    file_path = os.path.abspath(file_path)

    if attr_name is None:
        attr_name = file_name

    spec = importlib.util.spec_from_file_location(file_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, attr_name)

