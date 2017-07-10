"""Tests for embeddings module."""

import unittest
from vsmlib.corpus import load_as_ids, FileTokenIterator, DirTokenIterator
from vsmlib.vocabulary import Vocabulary_simple

# todo: use local vocab
path_vocab = "/work/alex/data/linguistic/embeddings/explicit/English/austen_m10_w2/"
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
        v = Vocabulary_simple()
        v.load(path_vocab)
        doc = load_as_ids(path_text, v)
        print(doc.shape)
        print(doc[:10])
