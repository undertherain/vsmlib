import os
import pandas
from pandas.io.json import json_normalize
from vsmlib.misc.data import load_json
from matplotlib import pyplot as plt


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


def plot_accuracy(path):
    df = df_from_dir(path)
    group = df.groupby(["experiment setup.category", "experiment setup.method"])
    means = group.mean()
    means.reset_index(inplace=True)
    means = means.loc[:, ["experiment setup.category", "experiment setup.method", "reciprocal_rank"]]
    unstacked = means.groupby(['experiment setup.category', 'experiment setup.method'])['reciprocal_rank'].aggregate('first').unstack()
    unstacked.plot(kind="bar")
    plt.show()


def main():
    path = "/mnt/storage/Data/linguistic/outs/BATS_3.0/"
    plot_accuracy(path)


if __name__ == "__main__":
    main()
