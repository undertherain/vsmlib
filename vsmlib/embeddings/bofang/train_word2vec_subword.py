#!/usr/bin/env python
"""Sample script of word embedding model.
This code implements skip-gram model and continuous-bow model.
"""
import argparse
import collections

import numpy as np
import six
import os

import chainer
from chainer import cuda
import chainer.functions as F
import chainer.initializers as I
import chainer.links as L
import chainer.optimizers as O
from chainer import reporter
from chainer import training
from chainer.training import extensions

import vsmlib
from vsmlib.vocabulary import Vocabulary
from vsmlib.vocabulary import create_from_dir
from vsmlib.corpus import load_file_as_ids
from vsmlib.model import ModelNumbered
from vsmlib.embeddings.bofang.subword import *


parser = argparse.ArgumentParser()
parser.add_argument('--gpu', '-g', default=-1, type=int,
                    help='GPU ID (negative value indicates CPU)')
parser.add_argument('--unit', '-u', default=100, type=int,
                    help='number of units')
parser.add_argument('--window', '-w', default=5, type=int,
                    help='window size')
parser.add_argument('--batchsize', '-b', type=int, default=1000,
                    help='learning minibatch size')
parser.add_argument('--epoch', '-e', default=1, type=int,
                    help='number of epochs to learn')
parser.add_argument('--model', '-m', choices=['skipgram'],
                    default='skipgram',
                    help='model type ("skipgram", "cbow")')
parser.add_argument('--subword', '-sw', choices=['none', 'rnn'],
                    default='rnn',
                    help='subword type ("none", "rnn")')
parser.add_argument('--maxWordLength', default=20, type=int,
                    help='max word length (for char-level subword only)')
parser.add_argument('--negative-size', default=5, type=int,
                    help='number of negative samples')
parser.add_argument('--out-type', '-o', choices=['hsm', 'ns', 'original'],
                    default='ns',
                    help='output model type ("hsm": hierarchical softmax, '
                    '"ns": negative sampling, "original": no approximation)')
parser.add_argument('--out', default='result',
                    help='Directory to output the result')
parser.add_argument('--path_corpus', default="/home/lbf/PycharmProjects/vsmlib/vsmlib/corpus/toy/",
                    help='path corpus, /home/lbf/PycharmProjects/vsmlib/vsmlib/corpus/toy/')
parser.add_argument('--test', dest='test', action='store_true')
parser.set_defaults(test=False)

args = parser.parse_args()

if args.gpu >= 0:
    chainer.cuda.get_device_from_id(args.gpu).use()
    cuda.check_cuda_available()

print('GPU: {}'.format(args.gpu))
print('# unit: {}'.format(args.unit))
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
            self.embed = L.EmbedID(
                n_vocab, n_units, initialW=I.Uniform(1. / n_units))
            self.loss_func = loss_func

    def __call__(self, x, context):
        e = self.embed(context)
        h = F.sum(e, axis=1) * (1. / context.shape[1])
        loss = self.loss_func(h, x)
        reporter.report({'loss': loss}, self)
        return loss

class RNN(chainer.Chain):
    def __init__(self, n_vocab_char, n_units,):
        super(RNN, self).__init__()
        with self.init_scope():
            self.embed = L.EmbedID(
                n_vocab_char, n_units, initialW=I.Uniform(1. / n_units))  # word embedding
            self.mid = L.LSTM(n_units, n_units)  # the first LSTM layer
            self.out = L.Linear(n_units, n_units)  # the feed-forward output layer

    def reset_state(self):
        self.mid.reset_state()

    def charRNN(self, context):  # input a list of word ids, output a list of word embeddings
        context_char = index2charIds[context]
        self.reset_state()
        for i in range(context_char.shape[1]):
            y = self(context_char[:, i])
        return y

    def __call__(self, cur_word, y_):
        # Given the current word ID, predict the next word.
        x = self.embed(cur_word)
        h = self.mid(x)
        y = self.out(h)
        return y

class SkipGram(chainer.Chain):

    def __init__(self, n_vocab, n_units, loss_func, n_vocab_char=None):
        super(SkipGram, self).__init__()

        with self.init_scope():
            if args.subword == 'none':
                self.embed = L.EmbedID(
                    n_vocab, n_units, initialW=I.Uniform(1. / n_units))
            if args.subword == 'rnn':
                self.rnn = RNN(n_vocab_char, n_units)
            self.loss_func = loss_func
    def getEmbeddings(self):
        if args.subword == 'rnn':
            return self.rnn.charRNN(range(n_vocab)).data
        if args.subword == 'none':
            return self.embed.W.data
        return None
    def __call__(self, x, context):

        x = F.broadcast_to(x[:, None], (context.shape[0], context.shape[1]))
        x = F.reshape(x, (context.shape[0] * context.shape[1],))

        if args.subword == 'rnn':
            context = context.reshape((context.shape[0] * context.shape[1]))
            e = self.rnn.charRNN(context)

        if args.subword == 'none':
            e = self.embed(context)
            e = F.reshape(e, (e.shape[0] * e.shape[1], e.shape[2]))

        loss = self.loss_func(e, x)
        reporter.report({'loss': loss}, self)
        return loss


class SkipGram_RNN(chainer.Chain):

    def __init__(self, n_vocab, n_units, loss_func):
        super(SkipGram_RNN, self).__init__()

        with self.init_scope():
            self.embed_char = L.EmbedID(
                n_vocab, n_units, initialW=I.Uniform(1. / n_units))
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


class WindowIterator(chainer.dataset.Iterator):

    def __init__(self, dataset, window, batch_size, repeat=True):
        self.dataset = np.array(dataset, np.int32)
        self.window = window
        self.batch_size = batch_size
        self._repeat = repeat

        self.order = np.random.permutation(
            len(dataset) - window * 2).astype(np.int32)
        self.order += window
        self.current_position = 0
        self.epoch = 0
        self.is_new_epoch = False

    def __next__(self):
        if not self._repeat and self.epoch > 0:
            raise StopIteration

        i = self.current_position
        i_end = i + self.batch_size
        position = self.order[i: i_end]
        w = np.random.randint(self.window - 1) + 1
        offset = np.concatenate([np.arange(-w, 0), np.arange(1, w + 1)])
        pos = position[:, None] + offset[None, :]
        context = self.dataset.take(pos)
        center = self.dataset.take(position)

        if i_end >= len(self.order):
            np.random.shuffle(self.order)
            self.epoch += 1
            self.is_new_epoch = True
            self.current_position = 0
        else:
            self.is_new_epoch = False
            self.current_position = i_end
        return center, context

    @property
    def epoch_detail(self):
        return self.epoch + float(self.current_position) / len(self.order)

    def serialize(self, serializer):
        self.current_position = serializer('current_position',
                                           self.current_position)
        self.epoch = serializer('epoch', self.epoch)
        self.is_new_epoch = serializer('is_new_epoch', self.is_new_epoch)
        if self._order is not None:
            serializer('_order', self._order)


def convert(batch, device):
    center, context = batch
    if device >= 0:
        center = cuda.to_gpu(center)
        context = cuda.to_gpu(context)
    return center, context


if args.gpu >= 0:
    cuda.get_device_from_id(args.gpu).use()

if args.path_corpus is None :
    train, val, _ = chainer.datasets.get_ptb_words()
    counts = collections.Counter(train)
    counts.update(collections.Counter(val))
    n_vocab = max(train) + 1
    vocab = chainer.datasets.get_ptb_words_vocabulary()
    index2word = {wid: word for word, wid in six.iteritems(vocab)}
else:
    def get_data(path, vocab):
        doc = load_file_as_ids(path, vocab)
        # doc = doc[doc >= 0]
        # smart split
        train, val = doc[:-1000], doc[-1000:]
        return train, val

    vocab = create_from_dir(args.path_corpus, min_frequency=10)
    train, val = get_data(os.path.join(args.path_corpus, "corpus"), vocab)
    word_counts = vocab.lst_frequencies
    n_vocab = vocab.cnt_words
    counts = {i: word_counts[i] for i in range(len(word_counts))}
    index2word = {i : vocab.lst_words[i] for i in range(len(vocab.lst_words))}


if args.test:
    train = train[:100]
    val = val[:100]

if args.subword == "rnn":
    index2charIds, vocab_char = get_chars(index2word, args.maxWordLength)
    n_vocab_char = len(vocab_char)

print('n_vocab: %d' % n_vocab)
print('data length: %d' % len(train))

if args.out_type == 'hsm':
    HSM = L.BinaryHierarchicalSoftmax
    tree = HSM.create_huffman_tree(counts)
    loss_func = HSM(args.unit, tree)
    loss_func.W.data[...] = 0
elif args.out_type == 'ns':
    cs = [counts[w] for w in range(len(counts))]
    loss_func = L.NegativeSampling(args.unit, cs, args.negative_size)
    loss_func.W.data[...] = 0
elif args.out_type == 'original':
    loss_func = SoftmaxCrossEntropyLoss(args.unit, n_vocab)
else:
    raise Exception('Unknown output type: {}'.format(args.out_type))

if args.model == 'skipgram':
    model = SkipGram(n_vocab, args.unit, loss_func, n_vocab_char)
elif args.model == 'cbow':
    model = ContinuousBoW(n_vocab, args.unit, loss_func)
else:
    raise Exception('Unknown model type: {}'.format(args.model))

if args.gpu >= 0:
    model.to_gpu()


optimizer = O.Adam()
optimizer.setup(model)

train_iter = WindowIterator(train, args.window, args.batchsize)
val_iter = WindowIterator(val, args.window, args.batchsize, repeat=False)
updater = training.StandardUpdater(
    train_iter, optimizer, converter=convert, device=args.gpu)
trainer = training.Trainer(updater, (args.epoch, 'epoch'), out=args.out)

trainer.extend(extensions.Evaluator(
    val_iter, model, converter=convert, device=args.gpu))
trainer.extend(extensions.LogReport())
trainer.extend(extensions.PrintReport(
    ['epoch', 'main/loss', 'validation/main/loss']))
trainer.extend(extensions.ProgressBar())
trainer.run()

with open('./result/word2vec.' + args.subword, 'w') as f:
    f.write('%d %d\n' % (len(index2word), args.unit))
    w = cuda.to_cpu(model.getEmbeddings())
    for i, wi in enumerate(w):
        v = ' '.join(map(str, wi))
        f.write('%s %s\n' % (index2word[i], v))
