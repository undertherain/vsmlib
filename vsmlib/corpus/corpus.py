import numpy as np
import fnmatch
import os


class FileTokenIterator:

    def __init__(self, path):
        self.path = path

    def __iter__(self):
        return self.next()

    def next(self):
        with open(self.path) as f:
            for line in f:
                for token in line.split():
                    yield token


class DirTokenIterator:
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        return self.next()

    def next(self):
        for root, dir, files in os.walk(self.path, followlinks=True):
            for items in fnmatch.filter(files, "*"):
                for token in FileTokenIterator(os.path.join(root, items)):
                    yield(token)


def load_as_ids(path, vocabulary, gzipped=None, downcase=True):
    # user proper tokenizer from cooc
    # options to ignore sentence bounbdaries
    # specify what to do with missing words
    # replace numbers with special tokens
    result = []
    with open(path) as f:
        for line in f:
            for token in line.split():
                w = token
                if downcase:
                    w = w.lower()
                result.append(vocabulary.get_id(w))
    return np.array(result, dtype=np.int32)


def main():
    print("test")
