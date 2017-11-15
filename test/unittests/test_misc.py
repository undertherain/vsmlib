"""Tests for misc"""
import unittest
from vsmlib.misc.deprecated import deprecated


@deprecated
def dummy():
    return 1


class Tests(unittest.TestCase):

    def test_deprecated(self):
        dummy()
