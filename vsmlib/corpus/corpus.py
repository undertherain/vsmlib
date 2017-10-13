import numpy as np
import fnmatch
import os
import re
from vsmlib.misc.data import detect_archive_format_and_open
import logging

logger = logging.getLogger(__name__)


class FileTokenIterator:

    def __init__(self, path):
        self.path = path
        re_pattern = r"[\w\-']+|[.,!?…]"
        self.re_token = re.compile(re_pattern)

    def __iter__(self):
        return self.next()

    def next(self):
        with detect_archive_format_and_open(self.path) as f:
            for line in f:
                s = line.strip().lower()
                # todo lower should be parameter
                tokens = self.re_token.findall(s)
                for token in tokens:
                    yield token


class DirTokenIterator:
    def __init__(self, path):
        self.path = path
        self.__gen__ = self.gen()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.__gen__)

    def gen(self):
        for root, dir, files in os.walk(self.path, followlinks=True):
            for items in fnmatch.filter(files, "*"):
                logger.info("processing " + os.path.join(root, items))
                for token in FileTokenIterator(os.path.join(root, items)):
                    yield(token)


def load_file_as_ids(path, vocabulary, gzipped=None, downcase=True):
    # use proper tokenizer from cooc
    # options to ignore sentence bounbdaries
    # specify what to do with missing words
    # replace numbers with special tokens
    result = []
    ti = FileTokenIterator(path)
    for token in ti:
        w = token    # specify what to do with missing words
        if downcase:
            w = w.lower()
        result.append(vocabulary.get_id(w))
    return np.array(result, dtype=np.int32)


def main():
    print("test")
