#!/usr/bin/env python
"""
Script of word embedding model with Character-level RNN information.

The character-level RNN is similar to the character model for machine traslation.
<Achieving Open Vocabulary Neural Machine Translation with Hybrid Word-Character Models>
https://pdfs.semanticscholar.org/0126/72696e5c1a1b06a2ba02fbfdb16bd24d920d.pdf?_ga=2.62596398.326349604.1504948983-92901532.1503389377

This code is based on the original chainer w2v implementation. 0ß
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
                    help='number of word vector units')
parser.add_argument('--unit_char', '-uc', default=100, type=int,
                    help='number of character vector units')
parser.add_argument('--window', '-w', default=5, type=int,
                    help='window size')
parser.add_argument('--batchsize', '-b', type=int, default=2000,
                    help='learning minibatch size')
parser.add_argument('--epoch', '-e', default=1, type=int,
                    help='number of epochs to learn')
parser.add_argument('--dropout', '-do', default=.2, type=int,
                    help='dropout ratio, zero indicates no dropout')
parser.add_argument('--model', '-m', choices=['skipgram'],
                    default='skipgram',
                    help='model type ("skipgram", "cbow")')
parser.add_argument('--subword', '-sw', choices=['none', 'rnn'],
                    default='none',
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
parser.add_argument('--dir_corpora', default="/home/lbf/PycharmProjects/vsmlib/vsmlib/corpus/100/",
                    help='dir corpora')
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
    def __init__(self, n_vocab_char, n_units, n_units_char):
        super(RNN, self).__init__()
        with self.init_scope():
            self.embed = L.EmbedID(
                n_vocab_char, n_units_char, initialW=I.Uniform(1. / n_units_char))  # word embedding
            self.mid = L.LSTM(n_units_char, n_units_char)  # the first LSTM layer
            self.out = L.Linear(n_units_char, n_units)  # the feed-forward output layer

    def reset_state(self):
        self.mid.reset_state()

    def charRNN(self, context):  # input a list of word ids, output a list of word embeddings
        # if chainer.config.train:
        #     print("train")
        # else:
        #     print("test")
        contexts2charIds = index2charIds[context]

        #sorting the context_char, make sure array length in descending order
        # ref: https://docs.chainer.org/en/stable/reference/generated/chainer.links.LSTM.html?highlight=Variable-length
        context_char_length = np.array([len(t) for t in contexts2charIds])
        argsort = context_char_length.argsort()[::-1] # descending order
        argsort_reverse = np.zeros(len(argsort), dtype=np.int32)  # this is used to restore the original order
        for i in range(len(argsort)):
            argsort_reverse[argsort[i]] = i
        contexts2charIds = contexts2charIds[context_char_length.argsort()[::-1]]

        #transpose a 2D list/numpy array
        rnn_inputs = [[] for i in range(len(contexts2charIds[0]))]
        for j in range(len(contexts2charIds)) :
            for i in range(len(contexts2charIds[j])):
                rnn_inputs[i].append(contexts2charIds[j][i])

        self.reset_state()
        for i in range(len(rnn_inputs)):
            y_ = self(np.array(rnn_inputs[i], np.int32))
        y = self.out(self.mid.h)
        y = y[argsort_reverse] # restore the original order
        return y

    def __call__(self, cur_word):
        # Given the current word ID, predict the next word.
        x = self.embed(cur_word)
        # dropout. ref: https://docs.chainer.org/en/stable/reference/generated/chainer.functions.dropout.html?highlight=dropout
        with chainer.using_config('train', True):
            x = F.dropout(x, args.dropout)
        h = self.mid(x)
        with chainer.using_config('train', True):
            h = F.dropout(h, args.dropout)
        y = self.out(h)
        return y

class SkipGram(chainer.Chain):

    def __init__(self, n_vocab, n_units, loss_func, n_vocab_char=None, n_units_char=None):
        super(SkipGram, self).__init__()

        with self.init_scope():
            if args.subword == 'none':
                self.embed = L.EmbedID(
                    n_vocab, n_units, initialW=I.Uniform(1. / n_units))
            if args.subword == 'rnn':
                self.rnn = RNN(n_vocab_char, n_units, n_units_char)
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

if args.dir_corpora is None :
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

    vocab = create_from_dir(args.dir_corpora, min_frequency=10)
    train, val = get_data(os.path.join(args.dir_corpora, "corpus"), vocab)
    word_counts = vocab.lst_frequencies
    n_vocab = vocab.cnt_words
    counts = {i: word_counts[i] for i in range(len(word_counts))}
    index2word = {i : vocab.lst_words[i] for i in range(len(vocab.lst_words))}


if args.test:
    train = train[:1000]
    val = val[:1000]

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
    if args.subword == 'none':
        model = SkipGram(n_vocab, args.unit, loss_func)
    if args.subword == "rnn":
        model = SkipGram(n_vocab, args.unit, loss_func, n_vocab_char, args.unit_char)
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

temp_dir = os.path.join('./result/' , args.subword, str(args.unit_char), os.path.basename(os.path.dirname(args.dir_corpora)))
if not os.path.isdir(temp_dir):
    os.makedirs(temp_dir)
with open(os.path.join(temp_dir, 'vec.txt'), 'w') as f:
    f.write('%d %d\n' % (len(index2word), args.unit))
    w = cuda.to_cpu(model.getEmbeddings())
    for i, wi in enumerate(w):
        v = ' '.join(map(str, wi))
        f.write('%s %s\n' % (index2word[i], v))
