"""Tests for w2v module."""

import unittest
import numpy as np
import vsmlib
import vsmlib.embeddings.train_word2vec
import argparse
from timeit import default_timer as timer
# from vsmlib.vocabulary import Vocabulary


path_text = "./test/data/corpora/plain/sense_small.txt"
path_vocab = "./test/data/vocab"


class Tests(unittest.TestCase):

    def test_ns(self):
        args = argparse.Namespace()
        args.test = True
        args.gpu = -1
        args.out_type = "ns"
        args.unit = 100
        args.negative_size = 5
        args.model = "skipgram"
        args.window = 4
        args.batchsize = 1000
        args.epoch = 10
        args.path_out = "/tmp/vsmlib/w2v"
        args.path_vocab = path_vocab
        args.path_text = path_text
        vsmlib.embeddings.train_word2vec.run(args)

    def test_hsm(self):
        args = argparse.Namespace()
        args.test = True
        args.gpu = -1
        args.out_type = "hsm"
        args.unit = 100
        args.negative_size = 5
        args.model = "skipgram"
        args.window = 4
        args.batchsize = 1000
        args.epoch = 10
        args.path_out = "/tmp/vsmlib/w2v"
        args.path_vocab = path_vocab
        args.path_text = path_text
        vsmlib.embeddings.train_word2vec.run(args)

    def test_iterator(self):
        dataset = np.arange(10000000)
        time_start = timer()
        cnt = 0
        it = vsmlib.embeddings.iter_simple.WindowIterator(dataset, window=5, batch_size=100)
        for i in range(2):
            sample = next(it)
            # print(sample)
            cnt += len(sample)
        time_end = timer()
        print("time: ", time_end - time_start)
