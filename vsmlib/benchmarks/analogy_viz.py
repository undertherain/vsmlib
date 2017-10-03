import os
import pandas
from pandas.io.json import json_normalize
from vsmlib.misc.data import load_json

path = "/mnt/storage/Data/linguistic/outs/BATS_3.0/LRCos_C1.0/w2v_bnc_vsm_w5_ns_normalized/D01 [noun+less_reg].json"


def df_from_file(path):
    data = load_json(path)
    for i in data["results"]:
        i.pop("predictions", None)
    meta = [["experiment setup", "category"], ["experiment setup", "method"]]
    df = json_normalize(data, record_path=["results"], meta=meta)
    return df


def df_from_dir(path):
    dfs = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for f in filenames:
            dfs.append(df_from_file(os.path.join(dirpath, f)))
    df = pandas.concat(dfs)
    return df

df = df_from_file(path)
print(df)
