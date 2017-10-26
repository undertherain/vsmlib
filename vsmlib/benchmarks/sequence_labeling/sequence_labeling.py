import numpy as np
from sklearn.linear_model import LogisticRegression
import sys
import yaml
from vsmlib.benchmarks.sequence_labeling import load_data
import argparse
import vsmlib


def contextwin(l, win):
    '''
    win :: int corresponding to the size of the window
    given a list of indexes composing a sentence
    it will return a list of list of indexes corresponding
    to context windows surrounding each word in the sentence
    '''
    assert win >=1
    l = list(l)
    # print((int)(win/2))
    lpadded = (int)(win) * [0] + l + (int)(win) * [0]
    out = [ lpadded[i:i + win * 2 + 1] for i in range(len(l)) ]

    assert len(out) == len(l)
    return out

'''
Get sequence labeling task's input and output.
'''
def getInputOutput(lex, y, win, idx2word):
    input = []
    output = []
    for i in range(len(lex)):
        wordListList = contextwin(lex[i], win)
        for j in range(len(wordListList)):
            wordList = wordListList[j]
            realWordList = [idx2word[word] for word in wordList]
            input.append(realWordList)
            output.append(y[i][j])
    return input, output


'''
get input (X) embeddings
'''
def getX(input, m):
    x = []

    random_vector = m.matrix.sum(axis=0)
    for wordList in input:
        v = []
        for word in wordList:
            if m.has_word(word):
                wv = m.get_row(word)
            else:
                wv = random_vector
            v.append(wv)
        v = np.array(v).flatten()
        x.append(v)

    return x

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--path_vectors', default='./../../../test/data/embeddings/npy/',
                        help='path to the embeddings')
    parser.add_argument('--path_dataset', default='./../../../test/data/benchmarks/sequence_labeling/',
                        help='path to the dataset')
    parser.add_argument('--window', '-w', default=2, type=int,
                        help='window size')

    args = parser.parse_args()
    return args

options = {}

def main():

    # use ArgumentParser
    # args = parse_args()

    # use yaml
    global options
    if len(sys.argv) > 1:
        path_config = sys.argv[1]
    else:
        print("usage: python3 -m vsmlib.benchmarls.sequence_labeling.sequence_labeling <config file>")
        print("config file example can be found at ")
        print("https://github.com/undertherain/vsmlib/blob/master/vsmlib/benchmarks/sequence_labeling/sequence_labeling/config.yaml")
        return

    with open(path_config, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    options["path_vectors"] = cfg["path_vectors"]
    options["path_dataset"] = cfg["path_dataset"]
    options["window"] = cfg["window"]


    # get the embeddings
    m = vsmlib.model.load_from_dir(options['path_vectors'])

    # get the dataset
    train_set, valid_set, test_set, dic = load_data.pos(options['path_dataset'])

    idx2label = dict((k, v) for v, k in dic['labels2idx'].items())
    idx2word = dict((k, v) for v, k in dic['words2idx'].items())

    train_lex, train_ne, train_y = train_set
    valid_lex, valid_ne, valid_y = valid_set
    test_lex, test_ne, test_y = test_set

    # add validation data to training data.
    train_lex.extend(valid_lex)
    train_ne.extend(valid_ne)
    train_y.extend(valid_y)

    vocsize = len(dic['words2idx'])
    nclasses = len(dic['labels2idx'])

    # get the training and test's input and output
    my_train_input, my_train_y = getInputOutput(train_lex, train_y, options['window'], idx2word)
    my_train_x = getX(my_train_input, m)
    my_test_input, my_test_y = getInputOutput(test_lex, test_y, options['window'], idx2word)
    my_test_x = getX(my_test_input, m)

    # fit LR classifier
    lrc = LogisticRegression()
    lrc.fit(my_train_x, my_train_y)

    # get results
    score_train = lrc.score(my_train_x, my_train_y)
    score_test = lrc.score(my_test_x, my_test_y)

    print("training set accuracy: %f" % (score_train))
    print("test set accuracy: %f" % (score_test))


if __name__ == '__main__':
    main()
