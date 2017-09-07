import numpy as np


def get_chars(index2word, maxWordLength) :
    index2charIds = [[] for i, w in index2word.items()] # np.zeros((len(index2word), maxWordLength), dtype=np.int32) - 1
    vocab_char = {}
    for i, w in index2word.items():
        charIds = []
        for j in range(min(len(w), maxWordLength)):
            # print(w[j] + " ")
            if w[j] not in vocab_char:
                vocab_char[w[j]] = len(vocab_char)
            index2charIds[i].append(vocab_char[w[j]])
    return np.array(index2charIds), vocab_char