"""Tests for vis module."""

import unittest
from vsmlib.visualize import draw_features_and_similarity
from vsmlib.model import ModelNumbered


class Tests(unittest.TestCase):

    def test_draw_features(self):
        model = ModelNumbered()
        path = "./test/data/embeddings/text/plain_with_file_header/emb.txt"
        model.load_from_text(path)
        draw_features_and_similarity(model, ["apple", "banana"])
