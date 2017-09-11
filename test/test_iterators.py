"""Tests for w2v module."""

import unittest
import numpy as np
import vsmlib
import vsmlib.embeddings
import vsmlib.embeddings.iter_simple
#from vsmlib.corpus import DirTokenIterator
from timeit import default_timer as timer


path_corpus = "./test/data/corpora/multiple_files"
path_vocab = "./test/data/vocab"


class Tests(unittest.TestCase):

    def test_iterator_legacy(self):
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

    def test_dir_iterator(self):
        iter = vsmlib.embeddings.iter_simple.DirWindowIterator(path=path_corpus, window_size=2, batch_size=4)
        cnt = 0
        for w in iter.token_iter:
            cnt += 1
        print(cnt, "words read")
