# convert text to array of indices
# or should we do this in vocabulary?

import numpy as np


def load_as_ids(path, vocabulary, gzipped=None):
    # user proper tokenizer from cooc
    # options to ignore sentence bounbdaries
    # specify what to do with missing words
    # downcase
    # replace numbers with special tokens
    result = []
    with open(path) as f:
        for line in f:
            for token in line.split():
                result.append(vocabulary.get_id(token))
    return np.array(result, dtype=np.int32)


def main():
    print("test")
