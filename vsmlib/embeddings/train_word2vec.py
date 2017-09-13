#!/usr/bin/env python3
"""Sample script of word embedding model.

This module implements skip-gram model and continuous-bow model.

"""
import argparse
import chainer
from chainer import cuda
import chainer.functions as F
import chainer.initializers as I
import chainer.links as L
from timeit import default_timer as timer
from chainer import reporter
from chainer import training
from chainer.training import extensions
import logging
import os
import vsmlib
from vsmlib.vocabulary import Vocabulary
from vsmlib.corpus import load_file_as_ids
from vsmlib.model import ModelNumbered
from .window_iterators import WindowIterator, DirWindowIterator


logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', '-g', default=-1, type=int,
                        help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--dimensions', '-d', default=100, type=int,
                        help='number of dimensions')
    parser.add_argument('--window', '-w', default=5, type=int,
                        help='window size')
    parser.add_argument('--batchsize', '-b', type=int, default=1000,
                        help='learning minibatch size')
    parser.add_argument('--epoch', '-e', default=20, type=int,
                        help='number of epochs to learn')
    parser.add_argument('--model', '-m', choices=['skipgram', 'cbow'],
                        default='skipgram', help='model type ("skipgram", "cbow")')
    parser.add_argument('--negative-size', default=5, type=int,
                        help='number of negative samples')
    parser.add_argument('--out_type', '-o', choices=['hsm', 'ns', 'original'],
                        default='hsm',
                        help='output model type ("hsm": hierarchical softmax, '
                        '"ns": negative sampling, "original": no approximation)')
    parser.add_argument('--path_corpus', help='path to the corpus', required=True)
    parser.add_argument('--path_vocab', help='path to the vocabulary', required=True)
    parser.add_argument('--path_out', help='path to save embeddings', required=True)
    parser.add_argument('--test', dest='test', default=False, action='store_true')

    args = parser.parse_args()
    return args


def print_params(args):
    print('GPU: {}'.format(args.gpu))
    print('dimensions: {}'.format(args.dimensions))
    print('Window: {}'.format(args.window))
    print('Minibatch-size: {}'.format(args.batchsize))
    print('# epoch: {}'.format(args.epoch))
    print('Training model: {}'.format(args.model))
    print('Output type: {}'.format(args.out_type))
    print('')


class ContinuousBoW(chainer.Chain):

    def __init__(self, n_vocab, n_units, loss_func):
        super(ContinuousBoW, self).__init__()

        with self.init_scope():
            self.embed = L.EmbedID(n_vocab, n_units, initialW=I.Uniform(1. / n_units))
            self.loss_func = loss_func

    def __call__(self, x, context):
        e = self.embed(context)
        h = F.sum(e, axis=1) * (1. / context.shape[1])
        loss = self.loss_func(h, x)
        reporter.report({'loss': loss}, self)
        return loss


class SkipGram(chainer.Chain):

    def __init__(self, n_vocab, n_units, loss_func):
        super(SkipGram, self).__init__()

        with self.init_scope():
            self.embed = L.EmbedID(n_vocab, n_units, initialW=I.Uniform(1. / n_units))
            self.loss_func = loss_func

    def __call__(self, x, context):
        e = self.embed(context)
        shape = e.shape
        x = F.broadcast_to(x[:, None], (shape[0], shape[1]))
        e = F.reshape(e, (shape[0] * shape[1], shape[2]))
        x = F.reshape(x, (shape[0] * shape[1],))
        loss = self.loss_func(e, x)
        reporter.report({'loss': loss}, self)
        return loss


class SoftmaxCrossEntropyLoss(chainer.Chain):

    def __init__(self, n_in, n_out):
        super(SoftmaxCrossEntropyLoss, self).__init__()
        with self.init_scope():
            self.out = L.Linear(n_in, n_out, initialW=0)

    def __call__(self, x, t):
        return F.softmax_cross_entropy(self.out(x), t)


def convert(batch, device):
    center, context = batch
    if device >= 0:
        center = cuda.to_gpu(center)
        context = cuda.to_gpu(context)
    return center, context


def save_w2v_legacy(args, model, index2word):
    with open('word2vec.model', 'w') as f:
        f.write('%d %d\n' % (len(index2word), args.dimensions))
        w = cuda.to_cpu(model.embed.W.data)
        for i, wi in enumerate(w):
            v = ' '.join(map(str, wi))
            f.write('%s %s\n' % (index2word[i], v))


def create_model(args, net, vocab):
    model = ModelNumbered()
    model.vocabulary = vocab
    model.metadata["vocabulary"] = vocab.metadata
    model.metadata.update(vars(args))
    model.metadata["vsmlib_version"] = vsmlib.__version__
    model.matrix = cuda.to_cpu(net.embed.W.data)
    return model


def get_data(path, vocab):
    doc = load_file_as_ids(path, vocab)
    # doc = doc[doc >= 0]
    # smart split
    train, val = doc[:-1000], doc[-1000:]
    return train, val


def run(args):
    time_start = timer()
    if args.gpu >= 0:
        chainer.cuda.get_device_from_id(args.gpu).use()
        cuda.check_cuda_available()

    vocab = Vocabulary()
    vocab.load(args.path_vocab)

    word_counts = vocab.lst_frequencies

    if args.out_type == 'hsm':
        HSM = L.BinaryHierarchicalSoftmax
        d_counts = {i: word_counts[i] for i in range(len(word_counts))}
        tree = HSM.create_huffman_tree(d_counts)
        loss_func = HSM(args.dimensions, tree)
        loss_func.W.data[...] = 0
    elif args.out_type == 'ns':
        cs = [word_counts[w] for w in range(len(word_counts))]
        loss_func = L.NegativeSampling(args.dimensions, cs, args.negative_size)
        loss_func.W.data[...] = 0
    elif args.out_type == 'original':
        loss_func = SoftmaxCrossEntropyLoss(args.dimensions, vocab.cnt_words)
    else:
        raise Exception('Unknown output type: {}'.format(args.out_type))

    if args.model == 'skipgram':
        model = SkipGram(vocab.cnt_words, args.dimensions, loss_func)
    elif args.model == 'cbow':
        model = ContinuousBoW(vocab.cnt_words, args.dimensions, loss_func)
    else:
        raise Exception('Unknown model type: {}'.format(args.model))

    if args.gpu >= 0:
        model.to_gpu()

    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)

    if os.path.isfile(args.path_corpus):
        train, val = get_data(args.path_corpus, vocab)
        if args.test:
            train = train[:100]
            val = val[:100]
        train_iter = WindowIterator(train, args.window, args.batchsize)
    else:
        train_iter = DirWindowIterator(path=args.path_corpus, vocab=vocab, window_size=args.window, batch_size=args.batchsize)
        return 
    # val_iter = WindowIterator(val, args.window, args.batchsize, repeat=False)
    updater = training.StandardUpdater(train_iter, optimizer, converter=convert, device=args.gpu)
    trainer = training.Trainer(updater, (args.epoch, 'epoch'), out=args.path_out)

    # trainer.extend(extensions.Evaluator(val_iter, model, converter=convert, device=args.gpu))
    trainer.extend(extensions.LogReport())
    trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'validation/main/loss', 'time']))
    trainer.extend(extensions.ProgressBar())
    trainer.run()
    # save(args, model, vocab.lst_words)
    model = create_model(args, model, vocab)
    time_end = timer()
    model.metadata["execution_time"] = time_end - time_start
    model.save_to_dir(args.path_out)
    logger.info("model saved to " + args.path_out)


def main():
    args = parse_args()
    print_params(args)
    run(args)


if __name__ == "__main__":
    main()
