import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import sys
import yaml
from vsmlib.benchmarks.sequence_labeling import load_data
import argparse
import vsmlib
from scipy.stats.stats import spearmanr
import os

def read_test_set(path):
    test = []
    with open(path) as f:
        for line in f:
            # line = line.lower();
            x, y, sim = line.strip().split()
            test.append(((x, y), float(sim)))
    return test

def evaluate(m, data):
    results = []
    for (x, y), sim in data:
        # print(x,y)
        if m.has_word(x) and m.has_word(y):
            # print(m.get_row(x).dot(m.get_row(y)))
            results.append((m.get_row(x).dot(m.get_row(y)), sim))
        else:
            pass
    actual, expected = zip(*results)
    return spearmanr(actual, expected)[0]

options = {}
def main(args=None):

    # use ArgumentParser
    # args = parse_args()

    # use yaml
    global options
    if args is None or args.path_config is None:
        if len(sys.argv) > 1:
            path_config = sys.argv[1]
        else:
            print("usage: python3 -m vsmlib.benchmarls.similarity.similarity <config file>")
            print("config file example can be found at ")
            print("https://github.com/undertherain/vsmlib/blob/master/vsmlib/benchmarks/sequence_labeling/similarity/config.yaml")
            return
    else:
        path_config = args.path_config

    with open(path_config, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    options["path_vector"] = cfg["path_vector"]
    options["path_dataset"] = cfg["path_dataset"]
    options["normalize"] = cfg["normalize"]

    # overwrite params
    if args is not None:
        if args.path_vector is not None:
            options["path_vector"] = args.path_vector
        if args.path_dataset is not None:
            options["path_dataset"] = args.path_dataset

    # get the embeddings
    m = vsmlib.model.load_from_dir(options['path_vector'])
    if options["normalize"]:
        # m.clip_negatives()  #make this configurable
        m.normalize()


    results = {}
    for file in os.listdir(options["path_dataset"]):
        testset = read_test_set(os.path.join(options["path_dataset"], file))
        result = evaluate(m, testset)
        results[os.path.splitext(file)[0]] = result
    print(results)
    return results


if __name__ == '__main__':
    main()
