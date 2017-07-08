# convert text to array of indices
# or should we do this in vocabulary?

import numpy as np


class FileIterator():

    def __init__(self, path):
        self.path = path

    def next(self):
        with open(self.path) as f:
            for line in f:
                for token in line.split():
                    yield token


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
