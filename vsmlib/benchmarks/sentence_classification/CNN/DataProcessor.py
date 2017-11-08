# -*- coding: utf-8 -*-
import os
import sys
import json
import numpy as np
from chainer import cuda
from collections import defaultdict


class DataProcessor(object):

    def __init__(self, data_path, test):
        self.train_data_path = os.path.join(data_path, "train.txt")
        self.dev_data_path = os.path.join(data_path, "dev.txt")
        self.test_data_path = os.path.join(data_path, "test.txt")
        self.test = test # if true, provide tiny datasets for quick test
        self.vocab = defaultdict(lambda: len(self.vocab))
        self.vocab["<pad>"]

    def prepare_dataset(self):
        # load train/dev/test data
        sys.stderr.write("loading dataset...")
        self.train_data = self.load_dataset("train")
        self.dev_data = self.load_dataset("dev")
        self.test_data = self.load_dataset("test")
        if self.test:
            sys.stderr.write("...preparing tiny dataset for quick test...")
            self.train_data = self.train_data[:100]
            self.dev_data = self.dev_data[:10]
        sys.stderr.write("done.\n")

    def load_dataset(self, _type):
        if _type == "train":
            path = self.train_data_path
        elif _type == "dev":
            path = self.dev_data_path
        else:
            path = self.test_data_path
        dataset = []
        with open(path, "r") as input_data:
            for line in input_data:
                polarity = line.strip().split()[0]
                y = np.array(polarity, dtype=np.int32)

                tokens = line.strip().split(" ")[1::]
                xs = np.array([self.vocab[token] for token in tokens], dtype=np.int32)
                #print(xs)
                dataset.append((xs, y))
        return dataset
