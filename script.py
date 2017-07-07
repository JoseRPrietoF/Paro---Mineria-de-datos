import pandas as pd
import numpy as np
import shutil, urllib, zipfile, os

path = "data/"
codificacion = 'cp1252'
def merge_csv(path):
    to_merge = []
    lst = os.listdir(path)
    lst.sort()
    data = None
    for file_name in lst:
        if not file_name.endswith(".csv"):
            continue
        filepath = os.path.join(path, file_name)
        print("Filepath %s " % filepath)
        df = pd.read_csv(filepath, sep=';', encoding=codificacion, error_bad_lines=False)

        if data is None: # first time
            data = df
            continue

        print(df.head())
        print(data.shape)
        exit()
        # 2016 (97404, 20)
    return pd.concat(to_merge)
df = merge_csv(path)
print(df.index)
print(df.iloc[1])
print(df.shape)
print(df.columns)