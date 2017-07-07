"""Tests for embeddings module."""

import unittest
from vsmlib.corpus import load_as_ids
from vsmlib.vocabulary import Vocabulary_simple

path_vocab = "/work/alex/data/linguistic/embeddings/explicit/English/austen_m10_w2/"
path_text = "/work/alex/data/linguistic/corpora/raw_texts/Eng/literature/austen/sense.txt"


class Tests(unittest.TestCase):

    def test_query_gpus(self):
        v = Vocabulary_simple()
        v.load(path_vocab)
        doc = load_as_ids(path_text, v)
        print(doc.shape)
        print(doc[:10])
