# -*- coding: utf-8 -*-
import sys
import chainer
import chainer.functions as F
import chainer.links as L
import numpy as np
from chainer import cuda, Function, Variable
from chainer import Link, Chain
import vsmlib


class CNN(Chain):

    def __init__(self, n_vocab, input_channel, output_channel, n_label, embed_dim, freeze, train=True):
        super(CNN, self).__init__(
            embed=L.EmbedID(n_vocab, embed_dim), 
            conv3=L.Convolution2D(
                input_channel, output_channel, (3, embed_dim)),
            conv4=L.Convolution2D(
                input_channel, output_channel, (4, embed_dim)),
            conv5=L.Convolution2D(
                input_channel, output_channel, (5, embed_dim)),
            l1=L.Linear(3 * output_channel, n_label)
        )
        self.train = train
        self.freeze = freeze

    def load_embeddings(self, emb_path, vocab):
        assert self.embed != None
        sys.stderr.write("loading word embedddings...")
        m = vsmlib.model.load_from_dir(emb_path)

        emb_ids = m.vocabulary.dic_words_ids.keys()
        dataset_ids = vocab.keys()

        for word in vocab.keys():
            if m.has_word(word.lower()):
                self.embed.W.data[vocab[word]] = m.get_row(word)
        print(self.embed.W.data.shape)
        sys.stderr.write("done\n")

    def __call__(self, xs):
        
        if self.freeze:
            self.embed.disable_update()
        xs = self.embed(xs)
        batchsize, height, width = xs.shape
        xs = F.reshape(xs, (batchsize, 1, height, width))
        conv3_xs = self.conv3(xs)
        conv4_xs = self.conv4(xs)
        conv5_xs = self.conv5(xs)
        h1 = F.max_pooling_2d(F.relu(conv3_xs), conv3_xs.shape[2])
        h2 = F.max_pooling_2d(F.relu(conv4_xs), conv4_xs.shape[2])
        h3 = F.max_pooling_2d(F.relu(conv5_xs), conv5_xs.shape[2])
        concat_layer = F.concat([h1, h2, h3], axis=1)
        with chainer.using_config('train', True):
            y = self.l1(F.dropout(F.tanh(concat_layer)))
        return y
