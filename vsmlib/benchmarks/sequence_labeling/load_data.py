import os

def load(path, task):
    dicts = {}
    dicts['labels2idx'] = {}
    dicts['words2idx'] = {}

    if task == 'pos':
        tag_position = 1
    elif task == 'chunk':
        tag_position = 2
    else:
        tag_position = -1

    for type in ["train", "test", "valid"] :
        with open(os.path.join(path, type + ".txt")) as f:
            for line in f:
                if len(line.strip()) is 0 :
                    continue
                lin = line.strip().split()
                word = lin[0]
                tag = lin[tag_position]
                word = word.lower()
                if word not in dicts['words2idx']:
                    dicts['words2idx'][word] = len(dicts['words2idx'])
                if tag not in dicts['labels2idx']:
                    dicts['labels2idx'][tag] = len(dicts['labels2idx'])


    out = {}
    for type in ["train", "test", "valid"] :
        w = []
        l = []
        ww = []
        ll = []
        with open(os.path.join(path, type + ".txt")) as f:
            for line in f:
                if len(line.strip()) is 0 :
                    if len(w) > 0:
                        ww.append(w)
                        ll.append(l)
                        w = []
                        l = []
                    continue
                lin = line.strip().split()
                word = lin[0].lower()
                tag = lin[tag_position]
                w.append(dicts['words2idx'][word])
                l.append(dicts['labels2idx'][tag])

        out[type] = (ww, ll)
    return out["train"], out["valid"], out["test"], dicts
