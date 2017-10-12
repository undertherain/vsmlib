import os
import pandas
from pandas.io.json import json_normalize
from vsmlib.misc.data import load_json
import matplotlib as mpl
from matplotlib import pyplot as plt


path = "/mnt/storage/Data/linguistic/outs/BATS_3.0/"


def df_from_file(path):
    data = load_json(path)
    for i in data["results"]:
        i.pop("predictions", None)
    meta = [["experiment setup", "category"], ["experiment setup", "method"]]
    df = json_normalize(data, record_path=["results"], meta=meta)
    df["reciprocal_rank"] = 1 / (df["rank"] + 1)
    return df


def df_from_dir(path):
    dfs = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for f in filenames:
            dfs.append(df_from_file(os.path.join(dirpath, f)))
    df = pandas.concat(dfs)
    return df

df = df_from_dir(path)
#print(df)
group = df.groupby(["experiment setup.category","experiment setup.method"])
means = group.mean()
#means.reset_index(inplace=True)
#group = means.groupby(["experiment setup.method"])
#dfs = [group.get_group(x) for x in group.groups]
#labels = set()
#for d in dfs:
#    labels.update(set(d["experiment setup.category"].unique()))
#    d.set_index("experiment setup.category",inplace=True)
#labels=sorted(list(labels))
#d=dfs[0]
print(means[:1])
#means.plot(kind='bar', x="experiment setup.category", y=["reciprocal_rank"], secondary_y=["experiment setup.method"] )
means.plot(kind='bar', x="experiment setup.category" )
plt.show()
