import os

def pos(path):
    dicts = {}
    dicts['labels2idx'] = {}
    dicts['words2idx'] = {}

    for type in ["train", "test", "valid"] :
        with open(os.path.join(path, type + ".txt")) as f:
            for line in f:
                if len(line.strip()) is 0 :
                    continue
                a, b, c, d = line.strip().split()
                a = a.lower()
                if a not in dicts['words2idx']:
                    dicts['words2idx'][a] = len(dicts['words2idx'])
                if b not in dicts['labels2idx']:
                    dicts['labels2idx'][b] = len(dicts['labels2idx'])

    out = {}
    for type in ["train", "test", "valid"] :
        w = []
        l = []
        o = []
        ww = []
        ll = []
        oo = []
        with open(os.path.join(path, type + ".txt")) as f:
            for line in f:
                if len(line.strip()) is 0 :
                    if len(w) > 0:
                        ww.append(w)
                        ll.append(l)
                        oo.append(o)
                        w = []
                        l = []
                        o = []
                    continue
                a, b, c, d = line.strip().split()
                a = a.lower()
                w.append(dicts['words2idx'][a])
                l.append(dicts['labels2idx'][b])
                o.append(0)
        out[type] = (ww, oo, ll)
    return out["train"], out["valid"], out["test"], dicts
