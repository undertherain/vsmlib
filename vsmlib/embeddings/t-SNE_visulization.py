import matplotlib
# matplotlib.use("GTK3Agg")
# matplotlib.use('pdf')
import argparse
import vsmlib.config
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_vector', help='path to the vector', required=True)
    parser.add_argument('--path_out', help='path to output', required=True)
    parser.add_argument('--central_word', help='the central word', default=None)
    parser.add_argument('--word_cnt', help='if central word is specified, select the nearst N words', default=25)

    args = parser.parse_args(args)
    return args

def get_word_and_index_list(central_word, cnt, m):
    # id = m.vocabulary.get_id(central_word)
    word_list_with_freq = m.get_most_similar_words(central_word, cnt=cnt)
    word_list = [w[0] for w in word_list_with_freq]
    index_list = [m.vocabulary.get_id(word) for word in word_list]
    return word_list, index_list


def run(args):
    args.central_word = 'physicists'
    args.path_vector = '/home/bofang/Documents/embeddings/final/_none/1/1/w3r/u300/e5/d0/'

    # '/home/bofang/Documents/embeddings/final_ner/cnn1d_none/1/1/w3r/u300/e3/d0/f/'

    # '/home/bofang/Documents/embeddings/final/sum_none/5/5/w3r/u300/e5/d0/f/'
    # '/home/bofang/Documents/embeddings/final/_none/1/1/w3r/u300/e5/d0/'
    # '/home/bofang/Documents/embeddings/final/bilstm_sum_none/1/1/w3r/u300/e5/d0/f/'

    m = vsmlib.model.load_from_dir(args.path_vector)
    m.normalize()

    if args.central_word is not None:
        word_list, index_list = get_word_and_index_list(args.central_word, args.word_cnt, m)
        matrix = m.matrix[index_list]
    else:
        matrix = m.matrix
        word_list = m.vocabulary.lst_words
    print(matrix.shape)


    np.set_printoptions(suppress=True)
    Y = TSNE(n_components=2, verbose=0).fit_transform(matrix)
    print(Y.shape)

    plt.scatter(Y[:, 0], Y[:, 1], alpha=0.0)
    for label, x, y in zip(word_list[1:], Y[1:, 0], Y[1:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(-40, 0), textcoords='offset points')
    if args.central_word is not None:
        plt.annotate(word_list[0], xy=(Y[0,0], Y[0,1]), xytext=(0, 0), textcoords='offset points', weight="bold")

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(4.5, 3.5)

    plt.axis('off')

    for title in ['none', 'sum', 'lstm', 'cnn']:
        if title in args.path_vector:
            if title == 'none':
                title = 'SGNS'
            title = title.upper()
            # plt.xlabel(title)
            # plt.title(title,)


    # plt.xticks([])
    # plt.yticks([])
    plt.tight_layout()
    fig.tight_layout()
    plt.show()
    # plt.savefig(args.path_out, format='pdf')


def main(args=None):
    args = parse_args(args)
    run(args)


if __name__ == "__main__":
    main()
