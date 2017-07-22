import os
import numpy as np
import time
from vsmlib._version import VERSION
from vsmlib.misc.formathelper import countof_fmt
from vsmlib.misc.data import save_json, load_json
from vsmlib.corpus import DirTokenIterator


class Vocabulary(object):

    def __init__(self):
        # todo: check if our ternary tree module is available
        self.dic_words_ids = {}
        self.lst_words = []
        self.metadata = {}

    def get_id(self, w):
        try:
            return self.dic_words_ids[w]
        except KeyError:
            return -1

    def get_word_by_id(self, i):
        return(self.lst_words[i])

    def get_frequency(self, i):
        if type(i) == str:
            i = self.get_id(i)
        if i < 0:
            return 0
        return(self.lst_frequencies[i])

    def save_to_dir(self, path):
        os.makedirs(path, exist_ok=True)
        f = open(os.path.join(path, "vocab.tsv"), "w")
        f.write("#word\tfrequency\n")
        for i in range(len(self.lst_words)):
            f.write("{}\t{}\n".format(self.lst_words[i], self.lst_frequencies[i]))
        f.close()
        save_json(self.metadata, os.path.join(path, "metadata.json"))

    def load(self, path):
        pos = 0
        f = open(os.path.join(path, "vocab.tsv"))
        self.lst_frequencies = []
        self.dic_words_ids = {}
        self.lst_words = []
        for line in f:
            if line.startswith("#"):
                continue
            word, frequency = line.split("\t")
            self.lst_words.append(word)
            self.lst_frequencies.append(int(frequency))
            self.dic_words_ids[word] = pos
            pos += 1
        f.close()
        self.cnt_words = len(self.lst_words)
        self.metadata = load_json(os.path.join(path, "metadata.json"))


class Vocabulary_simple(Vocabulary):

    def load_dic_from_file(self, filename):
        rdic = {}
        f = open(os.path.join(self.dir_root, filename),
                 encoding='utf-8', errors='replace')
        lines = f.readlines()
        for line in lines:
            tokens = line.split("\t")
            rdic[tokens[0]] = np.int64(tokens[-1])
        f.close()
        return rdic

    def load_list_from_file(self, filename, n):
        # postfix = 0
        self.lst_words = [""] * n
        # rdic={}
        # rlst=[]
        f = open(os.path.join(self.dir_root, filename),
                 encoding='utf-8', errors='replace')
        lines = f.readlines()
        for line in lines:
            tokens = line.split("\t")
        #    if tokens[0] in rdic:
            # rdic[tokens[0]+str(postfix)+tokens[1]]=np.int64(tokens[-1])
            # postfix+=1
            # else:
            # rdic[tokens[0]]=np.int64(tokens[-1])
            # rlst.append(tokens[0])
            self.lst_words[np.int64(tokens[-1])] = tokens[0]
        f.close()

    def load_list_from_sorted_file(self, filename):
        self.lst_words = []
        f = open(os.path.join(self.dir_root, filename),
                 encoding='utf-8', errors='replace')
        lines = f.readlines()
        for line in lines:
            token = line.strip()
            self.lst_words.append(token)
        f.close()

    def load(self, path, verbose=False):
        self.dir_root = path
        self.dic_words_ids = self.load_dic_from_file("ids")
        self.load_list_from_file("ids", len(self.dic_words_ids))
        if os.path.isfile(os.path.join(path, "freq_per_id")):
            f = open(os.path.join(self.dir_root, "freq_per_id"))
            self.lst_frequencies = np.fromfile(f, dtype=np.uint64)
            f.close()


class Vocabulary_cooccurrence(Vocabulary_simple):

    def load(self, path, verbose=False):
        t_start = time.time()
        Vocabulary_simple.load(self, path)
        t_end = time.time()
        # assert len(self.lst_words)==len(self.dic_words_ids)
        if verbose:
            cnt_words = len(self.lst_words)
            print("Vocabulary loaded in {0:0.2f} seconds".format(
                t_end - t_start))
            print("{} words ({}) in vocabulary".format(
                cnt_words, countof_fmt(cnt_words)))


# def report_rare():
        # for f in range(6):
            # cnt=0
            # for i in l_frequencies:
            # if i==f: cnt+=1
            # print ("words of frequency {}: {} of total {} - {:0.2f}%".format(f,countof_fmt(cnt), countof_fmt(len(l_frequencies)),100*cnt/len(l_frequencies)))

        # most_frequent = np.argsort(l_frequencies)[-10:]

def create_from_dir(path, min_frequency=0):
    dic_freqs = {}
    if not os.path.isdir(path):
        raise RuntimeError("source directory does not exist")
    for w in DirTokenIterator(path):
        if w in dic_freqs:
            dic_freqs[w] += 1
        else:
            dic_freqs[w] = 1
    v = Vocabulary_simple()
    v.lst_frequencies = []
    for i, word in enumerate(sorted(dic_freqs, key=dic_freqs.get, reverse=True)):
        frequency = dic_freqs[word]
        if frequency < min_frequency:
            break
        v.lst_frequencies.append(frequency)
        v.lst_words.append(word)
        v.dic_words_ids[word] = i
    v.cnt_words = len(v.lst_words)
    v.metadata["path_source"] = path
    v.metadata["min_frequency"] = min_frequency
    v.metadata["vsmlib_version"] = VERSION
    v.metadata["cnt_words"] = v.cnt_words
    return v
