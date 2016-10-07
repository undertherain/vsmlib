import numpy as np
import math
import scipy
from scipy import sparse
from vsmlib.vocabulary import get_id


def get_pmi_v(s):
    values = []
    idxs = s.nonzero()[1]
    for i in idxs:
        values.append([get_word_by_id(i), s[0, i]])
    values.sort(key=lambda tup: tup[1], reverse=True)
    return values


def get_pmi(w):
    id_w = get_id(w)
    if id_w < 0:
        return []
    #print("id = ",id_w)
    s = cooccurrence[id_w, :]
    return get_pmi_v(s)


def cmp_vectors(r1, r2):
    if sparse.issparse(r1):
        c = r1.dot(r2.T) / (np.linalg.norm(r1.data) * np.linalg.norm(r2.data))
        c = c[0, 0]
        if math.isnan(c):
            return 0
        return c
    else:
        c = scipy.spatial.distance.cosine(r1, r2)
        if math.isnan(c):
            return 0
        return 1 - c


def cmp_rows(id1, id2, m):
    if sparse.issparse(m):
        r1 = m[id1]  # .todense()
        r2 = m[id2]  # .todense()
    else:
        r1 = m[id1, :]
        r2 = m[id2, :]
    return cmp_vectors(r1, r2)


def cmp_words(w1, w2, m):
    id1 = get_id(w1)
    id2 = get_id(w2)
    if (id1 < 0) or (id2 < 0):
        return 0
    return cmp_rows(id1, id2, m)
