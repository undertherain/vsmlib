from vsmlib.vocabulary import Vocabulary_cooccurrence, Vocabulary_simple, Vocabulary
import vsmlib.matrix
import numpy as np
import scipy
from scipy import sparse
import scipy.sparse.linalg
import math
from matplotlib import pyplot as plt
import os
import brewer2mpl
import tables
import json
from .misc.formathelper import bcolors
from .misc.deprecated import deprecated
from .misc.data import save_json, load_json, detect_archive_format_and_open


def normed(v):
    return v / np.linalg.norm(v)


class Model(object):

    def __init__(self):
        self.provenance = ""
        self.name = ""
        self.metadata = {}

    def get_x_label(self, i):
        return self.vocabulary.get_word_by_id(i)

    def get_most_informative_columns(self, rows, width):
        xdim = rows.shape[1]
        scores = np.zeros(xdim)
        for i in range(rows.shape[0]):
            row = rows[i] / np.linalg.norm(rows[i])
            for j in range(len(row)):
                scores[j] += row[j]
        scores = abs(scores)
        tops = np.argsort(scores)
        return list(reversed(tops[-width:]))

    def filter_rows(self, ids_of_interest):
        # return (cooccurrence[1].todense()[:width])
        xdim = self.matrix.shape[1]
        dense = np.empty([0, xdim])
        # dense=np.empty([0,width])
        for i in ids_of_interest:
            if i < 0:
                continue
            if sparse.issparse(self.matrix):
                row = self.matrix[i].todense()
            else:
                row = self.matrix[i]
            row = np.asarray(row)
            row = np.reshape(row, (xdim))
            # dense=np.vstack([dense,row[:width]])
            dense = np.vstack([dense, row])
        return (dense)

    def filter_submatrix(self, lst_words_initial, width):
        words_of_interest = [
            w for w in lst_words_initial if self.vocabulary.get_id(w) >= 0]
        ids_of_interest = [self.vocabulary.get_id(
            w) for w in words_of_interest]
        rows = self.filter_rows(ids_of_interest)
        # xdim = rows.shape[1]
        # max_width = 25
        # width=min(xdim,max_width)
        vert = None  # np.empty((rows.shape[0],0))
        cols = self.get_most_informative_columns(rows, width)
        for i in cols:
            if vert is None:
                vert = (rows[:, i])
            else:
                vert = np.vstack([vert, rows[:, i]])
        labels = [self.get_x_label(i) for i in cols]
        return rows, vert.T, labels

    def get_most_similar_vectors(self, u, cnt=10):
        scores = np.zeros(self.matrix.shape[0], dtype=np.float32)
        for i in range(self.matrix.shape[0]):
            scores[i] = self.cmp_vectors(u, self.matrix[i])
        ids = np.argsort(scores)[::-1]
        ids = ids[:cnt]
        return zip(ids, scores[ids])

    def get_most_similar_words(self, w, cnt=10):
        if isinstance(w, str):
            vec = self.matrix[self.vocabulary.get_id(w)]
        else:
            vec = w
        rows = self.get_most_similar_vectors(vec, cnt)
        results = []
        for i in rows:
            results.append([self.vocabulary.get_word_by_id(i[0]), i[1]])
        return results

    def get_row(self, w):
        i = self.vocabulary.get_id(w)
        if i < 0:
            raise Exception('word do not exist', w)
            # return None
        row = self.matrix[i]
        return row

    def cmp_rows(self, id1, id2):
        r1 = self.matrix[id1]
        r2 = self.matrix[id2]
        return self.cmp_vectors(r1, r2)

    def cmp_words(self, w1, w2):
        id1 = self.vocabulary.get_id(w1)
        id2 = self.vocabulary.get_id(w2)
        if (id1 < 0) or (id2 < 0):
            return 0
        return self.cmp_rows(id1, id2)

    def load_props(self, path):
        try:
            with open(os.path.join(path, "props.json"), "r") as myfile:
                str_props = myfile.read()
                self.props = json.loads(str_props)
        except FileNotFoundError:
            print(bcolors.FAIL + "props.json not found" + bcolors.ENDC)
            self.props = {}
            # exit(-1)

    def load_provenance(self, path):
        try:
            with open(os.path.join(path, "provenance.txt"), "r") as myfile:
                self.provenance = myfile.read()
        except FileNotFoundError:
            print("provenance not found")
        self.load_props(path)


def normalize(m):
    for i in (range(m.shape[0] - 1)):
        norm = np.linalg.norm(m.data[m.indptr[i]:m.indptr[i + 1]])
        m.data[m.indptr[i]:m.indptr[i + 1]] /= norm


class Model_explicit(Model):
    def __init__(self):
        self.name += "explicit_"

    def cmp_vectors(self, r1, r2):
        c = r1.dot(r2.T) / (np.linalg.norm(r1.data) * np.linalg.norm(r2.data))
        c = c[0, 0]
        if math.isnan(c):
            return 0
        return c

    def load_from_hdf5(self, path):
        self.load_provenance(path)
        f = tables.open_file(os.path.join(path, 'cooccurrence_csr.h5p'), 'r')
        row_ptr = np.nan_to_num(f.root.row_ptr.read())
        col_ind = np.nan_to_num(f.root.col_ind.read())
        data = np.nan_to_num(f.root.data.read())
        dim = row_ptr.shape[0] - 1
        self.matrix = scipy.sparse.csr_matrix(
            (data, col_ind, row_ptr), shape=(dim, dim), dtype=np.float32)
        f.close()
        self.vocabulary = Vocabulary_cooccurrence()
        self.vocabulary.load(path)
        self.name += os.path.basename(os.path.normpath(path))

    def load(self, path):
        self.load_provenance(path)
        self.vocabulary = Vocabulary_cooccurrence()
        self.vocabulary.load(path)
        self.name += os.path.basename(os.path.normpath(path))
        self.matrix = vsmlib.matrix.load_matrix_csr(path, verbose=True)

    def clip_negatives(self):
        self.matrix.data.clip(0, out=self.matrix.data)
        self.matrix.eliminate_zeros()
        self.name += "_pos"
        self.provenance += "\ntransform : clip negative"

    def normalize(self):
        normalize(self.matrix)
        self.name += "_normalized"
        self.provenance += "\ntransform : normalize"
        self.normalized = True


class ModelDense(Model):

    def cmp_vectors(self, r1, r2):
        c = normed(r1) @ normed(r2)
        if math.isnan(c):
            return 0
        return c

    def save_matr_to_hdf5(self, path):
        f = tables.open_file(os.path.join(path, 'vectors.h5p'), 'w')
        atom = tables.Atom.from_dtype(self.matrix.dtype)
        ds = f.create_carray(f.root, 'vectors', atom, self.matrix.shape)
        ds[:] = self.matrix
        ds.flush()
        f.close()

    def load_hdf5(self, path):
        f = tables.open_file(os.path.join(path, 'vectors.h5p'), 'r')
        self.matrix = f.root.vectors.read()
        f.close()

    def save_to_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self.vocabulary.save_to_dir(path)
        # self.matrix.tofile(os.path.join(path,"vectors.bin"))
        # np.save(os.path.join(path, "vectors.npy"), self.matrix)
        self.save_matr_to_hdf5(path)
        save_json(self.metadata, os.path.join(path, "metadata.json"))

    def load_with_alpha(self, path, power=0.6, verbose=False):
        self.load_provenance(path)
        f = tables.open_file(os.path.join(path, 'vectors.h5p'), 'r')
#        left = np.nan_to_num(f.root.vectors.read())
        left = f.root.vectors.read()
        sigma = f.root.sigma.read()
        if verbose:
            print("loaded left singulat vectors and sigma")
        sigma = np.power(sigma, power)
        self.matrix = np.dot(left, np.diag(sigma))
        if verbose:
            print("computed the product")
        self.props["pow_sigma"] = power
        self.props["size_dimensions"] = self.matrix.shape[1]
        f.close()
        self.vocabulary = Vocabulary_simple()
        self.vocabulary.load(path)
        self.name += os.path.basename(os.path.normpath(path)) + "_a" + str(power)

    def load_from_dir(self, path):
        self.matrix = np.load(os.path.join(path, "vectors.npy"))
        # self.load_with_alpha(0.6)
        self.vocabulary = Vocabulary_simple()
        self.vocabulary.load(path)
        self.name += os.path.basename(os.path.normpath(path))
        self.load_provenance(path)

    def normalize(self):
        nrm = np.linalg.norm(self.matrix, axis=1)
        nrm[nrm == 0] = 1
        self.matrix /= nrm[:, np.newaxis]
        self.name += "_normalized"
        self.provenance += "\ntransform : normalized"
        self.props["normalized"] = True

    def load_from_text(self, path):
        i = 0
        # self.name+="_"+os.path.basename(os.path.normpath(path))
        self.vocabulary = vsmlib.vocabulary.Vocabulary()
        rows = []
        header = False
        with detect_archive_format_and_open(path) as f:
            for line in f:
                tokens = line.split()
                if i == 0 and len(tokens) == 2:
                    header = True
                    cnt_words = int(tokens[0])
                    size_embedding = int(tokens[1])
                    continue
                # word = tokens[0].decode('ascii',errors="ignore")
                # word = tokens[0].decode('UTF-8', errors="ignore")
                word = tokens[0]
                self.vocabulary.dic_words_ids[word] = i
                self.vocabulary.lst_words.append(word)
                str_vec = tokens[1:]
                row = np.zeros(len(str_vec), dtype=np.float32)
                for j in range(len(str_vec)):
                    row[j] = float(str_vec[j])
                rows.append(row)
                i += 1
        if header:
            assert cnt_words == len(rows)
        self.matrix = np.vstack(rows)
        if header:
            assert size_embedding == self.matrix.shape[1]
        self.vocabulary.lst_frequencies = np.zeros(len(self.vocabulary.lst_words))
        # self.name += "_{}".format(len(rows[0]))


class ModelNumbered(ModelDense):
    def get_x_label(self, i):
        return i

    def viz_wordlist(self, wl, colored=False, show_legend=False):
        colors = brewer2mpl.get_map('Set2', 'qualitative', 8).mpl_colors
        cnt = 0
        for i in wl:
            row = self.get_row(i)
            row = row / np.linalg.norm(row)
            if colored:
                plt.bar(range(0, len(row)), row, color=colors[cnt], linewidth=0, alpha=0.6, label=i)
            else:
                plt.bar(range(0, len(row)), row, color="black", linewidth=0, alpha=1 / len(wl), label=i)
            cnt += 1
        if show_legend:
            plt.legend()


class Model_Levi(ModelNumbered):
    def load_from_dir(self, path):
        self.name = "Levi_" + os.path.basename(os.path.normpath(path))
        self.matrix = np.load(os.path.join(path, "sgns.contexts.npy"))
        self.vocabulary = vsmlib.vocabulary.Vocabulary_simple()
        self.vocabulary.dir_root = path
        self.vocabulary.load_list_from_sorted_file(
            "/home/blackbird/data/scratch/Anna/w2-1000.iter1/sgns.words.vocab")
        self.vocabulary.dic_words_ids = {}
        for i in range(len(self.vocabulary.lst_words)):
            self.vocabulary.dic_words_ids[self.vocabulary.lst_words[i]] = i


class Model_svd_scipy(ModelNumbered):
    def __init__(self, original, cnt_singular_vectors, power):
        ut, s_ev, vt = scipy.sparse.linalg.svds(
            original.matrix, k=cnt_singular_vectors, which='LM')  # LM SM LA SA BE
        self.sigma = s_ev
        sigma_p = np.power(s_ev, power)
        self.matrix = np.dot(ut, np.diag(sigma_p))
        self.vocabulary = original.vocabulary
        self.provenance = original.provenance + \
            "\napplied scipy.linal.svd, {} singular vectors, sigma in the power of {}".format(
                cnt_singular_vectors, power)
        self.name = original.name + \
            "_svd_{}_C{}".format(cnt_singular_vectors, power)


class Model_w2v(ModelNumbered):
    @staticmethod
    def load_word(f):
        result = b''
        w = b''
        while w != b' ':
            w = f.read(1)
            result = result + w
        return result[:-1]

    def load_from_file(self, filename):
        self.vocabulary = Vocabulary()
        f = open(filename, "rb")
        header = f.readline().split()
        cnt_rows = int(header[0])
        size_row = int(header[1])
        self.name += "_{}".format(size_row)
        self.matrix = np.zeros((cnt_rows, size_row), dtype=np.float32)
        print("cnt rows = {}, size row = {}".format(cnt_rows, size_row))
        for i in range(cnt_rows):
            word = Model_w2v.load_word(f).decode(
                'UTF-8', errors="ignore").strip()
            # print (word)
            self.vocabulary.dic_words_ids[word] = i
            self.vocabulary.lst_words.append(word)
            s_row = f.read(size_row * 4)
            row = np.fromstring(s_row, dtype=np.float32)
            # row = row / np.linalg.norm(row)
            self.matrix[i] = row
        f.close()

    def load_from_dir(self, path):
        self.name += "w2v_" + os.path.basename(os.path.normpath(path))
        self.load_from_file(os.path.join(path, "vectors.bin"))
        self.load_provenance(path)


@deprecated
class Model_glove(ModelNumbered):
    def __init__(self):
        self.name = "glove"

    def load_from_dir(self, path):
        self.name = "glove_" + os.path.basename(os.path.normpath(path))
        files = os.listdir(path)
        for f in files:
            if f.endswith(".gz"):
                print("this is Glove")
                self.load_from_text(os.path.join(path, f))


def load_from_dir(path):
    if os.path.isfile(os.path.join(path, "cooccurrence_csr.h5p")):
        print("this is sparse explicit in hdf5")
        m = vsmlib.Model_explicit()
        m.load_from_hdf5(path)
        return m
    if os.path.isfile(os.path.join(path, "bigrams.data.bin")):
        print("this is sparse explicit")
        m = vsmlib.Model_explicit()
        m.load(path)
        return m
    if os.path.isfile(os.path.join(path, "vectors.bin")):
        print("this is w2v")
        m = vsmlib.Model_w2v()
        m.load_from_dir(path)
        return m
    if os.path.isfile(os.path.join(path, "sgns.words.npy")):
        m = Model_Levi()
        m.load_from_dir(path)
        print("this is Levi ")
        return m
    if os.path.isfile(os.path.join(path, "vectors.npy")):
        m = vsmlib.ModelNumbered()
        m.load_from_dir(path)
        print("this is dense ")
        return m
    if os.path.isfile(os.path.join(path, "vectors.h5p")):
        m = vsmlib.ModelNumbered()
        m.load_hdf5(path)
        print("this is vsmlib format ")
        return m

    m = ModelNumbered()
    files = os.listdir(path)
    for f in files:
        if f.endswith(".gz") or f.endswith(".bz") or f.endswith(".txt"):
            print("this is text")
            m.load_from_text(os.path.join(path, f))
            return m

    raise RuntimeError("can not detect embeddings format")
