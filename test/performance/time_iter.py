#!/usr/bin/python3

import unittest
#import cProfile, pstats, io
import vsmlib
import vsmlib.embeddings
import vsmlib.embeddings.window_iterators
from vsmlib.vocabulary import Vocabulary
from vsmlib.corpus import DirTokenIterator
from timeit import default_timer as timer
import logging

logging.basicConfig(level=logging.DEBUG)

# path_corpus = "/work/alex/data/linguistic/corpora/raw_texts/Eng/Wikipedia/EnWiki.2017.05"
# path_vocab = "/work/alex/data/linguistic/vocabs/bnc"
# path_corpus = "/work/alex/data/linguistic/corpora/raw_texts/Eng/literature/austen"
path_corpus = "/mnt/storage/Data/Corpora/raw_texts/brown"
path_vocab = "/mnt/storage/Data/linguistic/vocabs/bnc"


class Tests(unittest.TestCase):

    def test_time_dir_iter(self):
        cnt = 0
        time_start = timer()
        it = DirTokenIterator(path_corpus)
        for w in it:
            cnt += 1
        print(cnt, "words read")
        time_end = timer()
        print("dir iter time: ", time_end - time_start)


    def test_time_window_iter(self):
        time_start = timer()
        batch_size = 100
        vocab = Vocabulary()
        vocab.load(path_vocab)
        iter = vsmlib.embeddings.window_iterators.DirWindowIterator(path=path_corpus, vocab=vocab, window_size=5, batch_size=batch_size)
        print("iterating from dir:")
        cnt_iters = 0
        # pr = cProfile.Profile()
        # pr.enable()
        while iter.epoch < 1:
            next(iter)
            cnt_iters +=1
            if cnt_iters % 1000 == 0:
                print(iter.cnt_words_total)
        time_end = timer()
        #pr.disable()

        print("window iter time: ", time_end - time_start)
        print("tokens read: ", iter.cnt_words_total)
    #s = io.StringIO()
    #sortby = 'cumulative'
    #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    #ps.print_stats()
    #print(s.getvalue())

#def main():
#    time_dir_iter()
#    time_window_iter()

#if __name__ == "__main__":
#    main()
