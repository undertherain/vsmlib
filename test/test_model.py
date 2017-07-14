"""Tests for model module."""

import unittest
import vsmlib
from vsmlib.model import Model, ModelDense


class Tests(unittest.TestCase):

    def test_create(self):
        model = Model()
        self.assertIsInstance(model, object)

    def test_load(self):
        path = "/mnt/storage/Data/Embeddings/wikicorp/"
        # path = "/storage/embeddings/explicit_BNC_m100_w2_svd_d200"
        model = vsmlib.model.load_from_dir(path)
        self.assertIsInstance(model, object)
        print(model.name)

    def test_load_text(self):
        model = ModelDense()
        path = "/mnt/storage/Data/Embeddings/wikicorp/wikicorp.201004-pdc-iter-20-alpha-0.05-window-10-dim-50-neg-10-subsample-0.0001.txt.bz2"
        model.load_from_text(path)
        print(model.matrix.shape)

