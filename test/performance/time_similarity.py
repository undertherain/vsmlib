import numpy as np
from scipy.spatial.distance import cosine
from timeit import default_timer as timer

cnt_cols = 1000
cnt_rows = 100000

a = np.random.random((cnt_rows, cnt_cols)).astype(np.float32)
v = np.random.random(cnt_cols).astype(np.float32)
print(a.shape)
print(v.shape)


def normed(v):
    return v / np.linalg.norm(v)


def cmp_vectors(v1, v2):
    # c = cosine(normed(v1), normed(v2))
    # c = cosine(v1, v2)
    c = v1 @ v2
    return c


def get_sim_naive():
    # scores = np.zeros(cnt_rows, dtype=np.float32)
    scores = []
    for i in range(a.shape[0]):
        scores.append([cmp_vectors(v, a[i]), i])
    return scores


def get_sim_fast():
    scores = normed(v) @ a.T
    #scores = (scores + 1) / 2
    return scores

start = timer()
scores = get_sim_naive()
end = timer()
print("naive: ", end-start)


start = timer()
scores = get_sim_fast()
end = timer()
print("fast: ", end-start)
