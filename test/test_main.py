"""Tests for embeddings module."""

import unittest

from vsmlib.model import Model


class Tests(unittest.TestCase):

    def test_query_gpus(self):
        model = Model()
        self.assertIsInstance(model, object)
