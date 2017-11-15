"""Tests for misc"""
import unittest
import logging
from vsmlib.misc.deprecated import deprecated
logger = logging.getLogger(__name__)


@deprecated
def dummy():
    return 1


class Tests(unittest.TestCase):

    def test_deprecated(self):
        logger.info("testing deprecated")
        dummy()
