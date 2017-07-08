"""Tests for embeddings module."""

import unittest

import vsmlib
# from vsmlib.model import Model


class Tests(unittest.TestCase):

    def test_load(self):
        model = vsmlib.model.load_from_dir("/storage/embeddings/explicit_BNC_m100_w2_svd_d200")
        self.assertIsInstance(model, object)
        print(model.name)
