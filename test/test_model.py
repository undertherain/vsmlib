"""Tests for model module."""

import unittest
import vsmlib
from vsmlib.model import Model, ModelDense


class Tests(unittest.TestCase):

    def test_create(self):
        model = ModelDense()
        self.assertIsInstance(model, Model)

    def test_load_plain_text(self):
        model = ModelDense()
        path = "./test/data/embeddings/text/plain/emb.txt"
        model.load_from_text(path)
        print(model.matrix.shape)

    def test_load(self):
        path = "./test/data/embeddings/text/plain/"
        model = vsmlib.model.load_from_dir(path)
        self.assertIsInstance(model, Model)
        print(model.name)

    def test_save(self):
        path = "./test/data/embeddings/text/plain/"
        model = vsmlib.model.load_from_dir(path)
        path_save = "/tmp/vsmlib/saved"
        model.save_to_dir(path_save)
        model = vsmlib.model.load_from_dir(path_save)
        print(model.matrix.shape)
