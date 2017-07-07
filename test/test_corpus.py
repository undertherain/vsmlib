"""Tests for embeddings module."""

import unittest

from vsmlib.corpus import load_as_ids


class Tests(unittest.TestCase):

    def test_query_gpus(self):
        load_as_ids("/dev/null", {})
