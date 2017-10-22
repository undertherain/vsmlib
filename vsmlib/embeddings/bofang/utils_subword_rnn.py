import chainer
import chainer.functions as F
import chainer.initializers as I
import chainer.links as L
from chainer import reporter
from vsmlib.embeddings.bofang.subword import *



"""
Script of word embedding model with Character-level RNN information.

The character-level RNN is similar to the character model for machine traslation.
<Achieving Open Vocabulary Neural Machine Translation with Hybrid Word-Character Models>
https://pdfs.semanticscholar.org/0126/72696e5c1a1b06a2ba02fbfdb16bd24d920d.pdf?_ga=2.62596398.326349604.1504948983-92901532.1503389377

This code is based on the original chainer w2v implementation. 0ß
"""

class RNN(chainer.Chain):
    def __init__(self, n_vocab_char, n_units, n_units_char, index2charIds, dropout=.2):  #dropout ratio, zero indicates no dropout
        super(RNN, self).__init__()
        with self.init_scope():
            self.embed = L.EmbedID(
                n_vocab_char, n_units_char, initialW=I.Uniform(1. / n_units_char))  # word embedding
            self.mid = L.LSTM(n_units_char, n_units_char)  # the first LSTM layer
            self.out = L.Linear(n_units_char, n_units)  # the feed-forward output layer
            self.dropout = dropout
            self.index2charIds = index2charIds

    def reset_state(self):
        self.mid.reset_state()

    def charRNN(self, context):  # input a list of word ids, output a list of word embeddings
        # if chainer.config.train:
        #     print("train")
        # else:
        #     print("test")
        contexts2charIds = self.index2charIds[context]

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
            x = F.dropout(x, self.dropout)
        h = self.mid(x)
        with chainer.using_config('train', True):
            h = F.dropout(h, self.dropout)
        y = self.out(h)
        return y


class SkipGram(chainer.Chain):

    def __init__(self, vocab, maxWordLength, dimensions, loss_func):
        super(SkipGram, self).__init__()

        with self.init_scope():
            index2word = {i: vocab.lst_words[i] for i in range(len(vocab.lst_words))}
            index2charIds, vocab_char = get_chars(index2word, maxWordLength)
            n_vocab_char = len(vocab_char)
            self.rnn = RNN(n_vocab_char, dimensions, dimensions, index2charIds)

            self.loss_func = loss_func
            self.n_vocab = len(index2word)

    def getEmbeddings(self):
        return self.rnn.charRNN(range(self.n_vocab)).data
    def __call__(self, x, context):

        x = F.broadcast_to(x[:, None], (context.shape[0], context.shape[1]))
        x = F.reshape(x, (context.shape[0] * context.shape[1],))

        context = context.reshape((context.shape[0] * context.shape[1]))
        e = self.rnn.charRNN(context)

        loss = self.loss_func(e, x)
        reporter.report({'loss': loss}, self)
        return loss



class ContinuousBoW(chainer.Chain):

    def __init__(self, vocab, maxWordLength, dimensions, loss_func):
        super(ContinuousBoW, self).__init__()

        with self.init_scope():
            index2word = {i: vocab.lst_words[i] for i in range(len(vocab.lst_words))}
            index2charIds, vocab_char = get_chars(index2word, maxWordLength)
            n_vocab_char = len(vocab_char)
            self.rnn = RNN(n_vocab_char, dimensions, dimensions, index2charIds)

            self.loss_func = loss_func
            self.n_vocab = len(index2word)

    def getEmbeddings(self):
        return self.rnn.charRNN(range(self.n_vocab)).data
    def __call__(self, x, context):
        context_shape = context.shape

        context = context.reshape((context.shape[0] * context.shape[1]))
        e = self.rnn.charRNN(context)

        e = F.reshape(e, (context_shape[0], context_shape[1], e.shape[1]))

        h = F.sum(e, axis=1) * (1. / context_shape[1])

        loss = self.loss_func(h, x)
        reporter.report({'loss': loss}, self)
        return loss
