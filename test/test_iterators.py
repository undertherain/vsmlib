"""Tests for w2v module."""

import unittest
import numpy as np
import vsmlib
from timeit import default_timer as timer


path_corpus = "./test/data/corpora/plain/sense_small.txt"
path_vocab = "./test/data/vocab"


class Tests(unittest.TestCase):

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
