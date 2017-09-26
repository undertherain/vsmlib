"""Tests for w2v module."""

import unittest
import vsmlib
import vsmlib.embeddings.train_word2vec
import argparse


path_text = "./test/data/corpora/plain/sense_small.txt"
path_vocab = "./test/data/vocabs/plain"
path_muliple = "./test/data/corpora/multiple_files"


class Tests(unittest.TestCase):

    def test_ns(self):
        args = argparse.Namespace()
        args.test = True
        args.gpu = -1
        args.out_type = "ns"
        args.dimensions = 100
        args.negative_size = 5
        args.model = "skipgram"
        args.window = 4
        args.batchsize = 1000
        args.epoch = 10
        args.path_out = "/tmp/vsmlib/w2v"
        args.path_vocab = path_vocab
        args.path_corpus = path_text
        vsmlib.embeddings.train_word2vec.run(args)

    def test_hsm(self):
        args = argparse.Namespace()
        args.test = True
        args.gpu = -1
        args.out_type = "hsm"
        args.dimensions = 100
        args.negative_size = 5
        args.model = "skipgram"
        args.window = 4
        args.batchsize = 1000
        args.epoch = 10
        args.path_out = "/tmp/vsmlib/w2v"
        args.path_vocab = path_vocab
        args.path_corpus = path_text
        vsmlib.embeddings.train_word2vec.run(args)

    def test_dir_iter(self):
        args = argparse.Namespace()
        args.test = True
        args.gpu = -1
        args.out_type = "ns"
        args.dimensions = 100
        args.negative_size = 5
        args.model = "skipgram"
        args.window = 4
        args.batchsize = 1000
        args.epoch = 10
        args.path_out = "/tmp/vsmlib/w2v"
        args.path_vocab = path_vocab
        args.path_corpus = path_muliple
        vsmlib.embeddings.train_word2vec.run(args)

    def test_empty_dir_iter(self):
        args = argparse.Namespace()
        args.test = True
        args.gpu = -1
        args.out_type = "ns"
        args.dimensions = 100
        args.negative_size = 5
        args.model = "skipgram"
        args.window = 4
        args.batchsize = 1000
        args.epoch = 10
        args.path_out = "/tmp/vsmlib/w2v"
        args.path_vocab = path_vocab
        args.path_corpus = "./test/data/corpora/empty"
        try:
            vsmlib.embeddings.train_word2vec.run(args)
        except RuntimeError:
            print("corpus empty exception caught")
