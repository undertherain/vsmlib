"""Tests for w2v module."""

import unittest
import numpy as np
import vsmlib
import vsmlib.embeddings
import vsmlib.embeddings.window_iterators
from vsmlib.vocabulary import Vocabulary
from timeit import default_timer as timer


path_corpus = "./test/data/corpora/multiple_small"
path_vocab = "./test/data/vocabs/numbers"


class Tests(unittest.TestCase):

    def test_iterator_legacy_timing(self):
        cnt_tokens = 1000000
        dataset = np.arange(cnt_tokens)
        time_start = timer()
        cnt = 0
        batch_size = 100
        it = vsmlib.embeddings.window_iterators.WindowIterator(dataset, window=2, batch_size=batch_size)
        for i in range(cnt_tokens // batch_size):
            sample = next(it)
            cnt += len(sample)
        time_end = timer()
        print("time: ", time_end - time_start)

    def test_iterator_legacy_debug_print(self):
        dataset = np.arange(1000)
        it = vsmlib.embeddings.window_iterators.WindowIterator(dataset, window=3, batch_size=1)
        sample = next(it)
        print("batch from legacy:")
        for i in sample:
            print(i)

    def test_dir_iterator_debug_print(self):
        vocab = Vocabulary()
        vocab.load(path_vocab)
        iter = vsmlib.embeddings.window_iterators.DirWindowIterator(path=path_corpus, vocab=vocab, window_size=3, batch_size=2)
        print("batch from dir:")
        for i in range(2):
            sample = next(iter)
            for i in sample:
                print(i)
