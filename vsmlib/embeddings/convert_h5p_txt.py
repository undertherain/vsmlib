"""

this script evaluate all available benchmarks on vsmlib

"""
import argparse
import os
import sys
from vsmlib.benchmarks.analogy import analogy
from vsmlib.benchmarks.similarity import similarity
from vsmlib.benchmarks.sequence_labeling import sequence_labeling
import json
import vsmlib.config
from multiprocessing import Pool
from multiprocessing import Process
import copy


def run(path):
    if not os.path.isfile(os.path.join(path, "vectors.h5p")) and not os.path.isfile(os.path.join(path, "vectors.txt")):
        return
    if os.path.isfile(os.path.join(path, "vectorsb.txt")):
        return
    if 'context' in path:
        return

    m = vsmlib.model.load_from_dir(path)
    m.normalize()

    print(path)
    with open(os.path.join(path, "vectorsb.txt"), 'w') as output:
        for k, v in m.vocabulary.dic_words_ids.items():
            output.write(k + " ")
            for f in m.matrix[v]:
                output.write(str(f))
                output.write(" ")
            output.write("\r\n")


def main():
    path_vector = "/home/bofang/Documents/embeddings/final_ner/"
    # path_vector = '/home/bofang/Documents/embeddings/text8/_none/1/1/w3r/u300/e3/'

    for root, dirs, files in os.walk(path_vector, topdown=False):
        for name in dirs:
            path = os.path.join(root, name)
            run(path)



if __name__ == "__main__":
    main()
