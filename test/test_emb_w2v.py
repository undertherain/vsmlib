"""Tests for w2v module."""

import unittest
import vsmlib
import vsmlib.embeddings.train_word2vec
import argparse
# from vsmlib.vocabulary import Vocabulary


path_text = "./test/data/corpora/plain/sense_small.txt"
path_vocab = "./test/data/vocab"


class Tests(unittest.TestCase):

    def test_create_from_file(self):
        args = argparse.Namespace()
        args.test = True
        args.gpu = -1
        args.out_type = "ns"
        args.unit = 100
        args.negative_size = 5
        args.model = "skipgram"
        args.window = 5
        args.batchsize = 1000
        args.epoch = 20
        args.path_out = "/tmp/vsmlib/w2v"
        args.path_vocab = path_vocab
        args.path_text = path_text
        vsmlib.embeddings.train_word2vec.run(args)
