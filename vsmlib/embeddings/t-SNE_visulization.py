import argparse
import vsmlib.config
from sklearn.manifold import TSNE
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_vector', help='path to the vector', required=True)
    parser.add_argument('--path_out', help='path to output', required=True)

    args = parser.parse_args(args)
    return args


def run(args):
    m = vsmlib.model.load_from_dir(args.path_vector)
    m.normalize()
    print(m.matrix.shape)

    np.set_printoptions(suppress=True)
    Y = TSNE(n_components=2, verbose=1).fit_transform(m.matrix)
    print(Y.shape)

    plt.scatter(Y[:, 0], Y[:, 1], alpha=0.0)
    for label, x, y in zip(m.vocabulary.lst_words, Y[:, 0], Y[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.show()
    # plt.savefig(args.path_out, format='eps')


def main(args=None):
    args = parse_args(args)
    run(args)


if __name__ == "__main__":
    main()
