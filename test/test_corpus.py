"""Tests for embeddings module."""

import unittest
from vsmlib.corpus import load_file_as_ids, FileTokenIterator, DirTokenIterator
from vsmlib.vocabulary import Vocabulary

# todo: use local vocab
path_vocab = "./test/data/vocab"
path_text = "./test/data/corpora/small"
path_text_file = "./test/data/corpora/small/sense_small.txt"


class Tests(unittest.TestCase):

    def test_file_iter(self):
        cnt = 0
        for w in (FileTokenIterator(path_text_file)):
            cnt += 1
        print(cnt, "words read")

    def test_dir_iter(self):
        cnt = 0
        for w in (DirTokenIterator(path_text)):
            cnt += 1
        print(cnt, "words read")

    def test_text_to_ids(self):
        v = Vocabulary()
        v.load(path_vocab)
        doc = load_file_as_ids(path_text_file, v)
        print(doc.shape)
        print(doc[:10])
