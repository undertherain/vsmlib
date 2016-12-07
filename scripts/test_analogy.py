import numpy as np
import math
import random
import scipy
from tqdm import tqdm
import os
import fnmatch
import sklearn
from sklearn.linear_model import LogisticRegression
import re
import datetime
import json
import csv
import sys
sys.path.append("..")
import vsmlib
import yaml

options = {}


dir_out = "out"
do_top5 = True


# this are some hard-coded bits which will be implemented later
need_subsample = False
size_cv_test = 1
set_aprimes_test = None
inverse_regularization_strength = 1.0

# options["degree"]=3
# name_method="SVMCos"
# name_kernel="linear"
# name_kernel="poly"
# name_kernel='rbf'


class Session:

    def __init__(self):
        self.name = str(datetime.datetime.now()) + " " + options["name_method"]
        self.files = {}

    def acumulate(keys, values):
        for key in keys:
            pass

    def append_vals_to_csv(self, name_file, vals):
        keys = sorted(list(vals.keys()))
        name_file_full = "sessions/" + self.name + "/" + name_file
        if name_file_full not in self.files:
            if not os.path.exists(os.path.dirname(name_file_full)):
                os.makedirs(os.path.dirname(name_file_full))
            if not os.path.exists(name_file_full):
                fd = open(name_file_full, 'w')
                self.files[name_file_full] = fd
                writer_csv = csv.writer(
                    fd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer_csv.writerow(keys)
        # else:
        writer_csv = csv.writer(
            self.files[name_file_full],
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)
        vs = [vals[key] for key in keys]
        writer_csv.writerow(vs)
        #str_row=','.join(map(str, vs))
        # self.files[name_file].write(str_row+"\n")
        # fd.close()

    def __del__(self):
        for key in self.files:
            self.files[key].close()

    def flush(self):
        for key in self.files:
            self.files[key].close()
            self.files[key] = open(key, 'a')
# session=Session()


def get_most_similar_fast(v):
    scores = v @ m_normed.T
    return scores

# def get_most_similar_sparse(v)


def get_most_collinear_fast(a, ap, b):
    scores = np.zeros(m.matrix.shape[0])
    offset_target = ap - a
    offset_target = offset_target / np.linalg.norm(offset_target)
    m_diff = m.matrix - b
    norm = np.linalg.norm(m_diff, axis=1)
    norm[norm == 0] = 100500
    m_diff /= norm[:, None]
    scores = m_diff @ offset_target
    return scores


def is_pair_missing(pair):
    if m.vocabulary.get_id(pair[0]) < 0:
        return True
    # if m.vocabulary.get_id(pair[0,0])<0: return True
#    for entry in pair:
#        for token in entry:
#            if m.vocabulary.get_id(token)<0: return True
    return False


def is_quad_missing(quad):
    if m.vocabulary.get_id(quad[0]) < 0:
        return True
    if m.vocabulary.get_id(quad[2]) < 0:
        return True
    if m.vocabulary.get_id(quad[1][0]) < 0:
        return True
    if m.vocabulary.get_id(quad[3][0]) < 0:
        return True
    return False


def gen_vec_single(pairs):
    a, a_prime = zip(*pairs)
    a_prime = [i[0] for i in a_prime]
    #a_prime=[i for sublist in a_prime for i in sublist]
    a_prime = [i for i in a_prime if m.vocabulary.get_id(i) >= 0]
    noise = [random.choice(m.vocabulary.lst_words) for i in range(len(a))]
    x = list(a_prime) + list(a) + list(a) + list(a) + list(a) + noise
    X = np.array([m.get_row(i) for i in x])
    Y = np.hstack([np.ones(len(a_prime)), np.zeros(len(x) - len(a_prime))])
    return X, Y


def gen_vec_single_nonoise(pairs):
    a, a_prime = zip(*pairs)
    a_prime = [i for sublist in a_prime for i in sublist]
    a_prime = [i for i in a_prime if m.vocabulary.get_id(i) >= 0]
    x = list(a_prime) + list(a)
    X = np.array([m.get_row(i) for i in x])
    Y = np.hstack([np.ones(len(a_prime)), np.zeros(len(x) - len(a_prime))])
    return X, Y


def trivial(a):
    return a
try:
    profile
except NameError:
    profile = trivial


def do_test_on_pair_3CosAdd(pairs_test, pairs_train, file_out):
    cnt_total = 0
    cnt_correct = 0
    for p_test in pairs_test:
        for p_train in pairs_train:
            cnt_total += 1
            #quad = p_test + p_train
            #quad = p_train + p_test
            #print ("iterating p_train")
            if is_quad_missing(p_train + p_test):
                # cnt_missing+=1;
                # file_out.write("{}\t{}\t{}\t{}\t{}\n".format(quad[0],quad[1],quad[2],quad[3],"MISSSING"))
                continue
#            print ("doing {} - {} + {}".format(quad[1][0],quad[0],quad[2]))
            vec_a = m.get_row(p_train[0])
            vec_a_prime = m.get_row(p_train[1][0])
            vec_b = m.get_row(p_test[0])
            
            if scipy.sparse.issparse(m_normed):
                vec_a = vec_a.toarray()[0]
                vec_a_prime = vec_a_prime.toarray()[0]
                vec_b = vec_b.toarray()[0]

            # file_out.write("{}\t{}\t{}\t".format(quad[0],quad[1],quad[2]))
            if options["name_method"] == "3CosAdd":
                vec_b_prime = vec_a_prime - vec_a + vec_b
                vec_b_prime /= np.linalg.norm(vec_b_prime)
                scores = get_most_similar_fast(vec_b_prime)
            else:
                scores = get_most_collinear_fast(vec_a, vec_a_prime, vec_b)
            ids_max = np.argsort(scores)[::-1]
            is_hit = False
            #print ("about to report results")
            #ids_question = {
                #m.vocabulary.get_id(
                    #quad[0]), m.vocabulary.get_id(
                    #quad[2])}
            #for z in quad[1]:
                #ids_question.add(m.vocabulary.get_id(z))
            #print (ids_question)
            #,m.vocabulary.get_id(quad[1])}#,m.vocabulary.get_id(quad[2])}
            #b_prime = quad[3]
            #b_primes = [i.strip() for i in b_prime]
            #extr="as {} to {}".format(p_train[0],p_train[1])
            process_prediction(p_test, scores, None, None, file_out, p_train)

    return cnt_total, cnt_correct


def create_list_test_right(pairs):
    global set_aprimes_test
    a, a_prime = zip(*pairs)
    a_prime = [i for sublist in a_prime for i in sublist]
    set_aprimes_test = set(a_prime)


def process_prediction(
        p_test_one,
        scores,
        score_reg,
        score_sim,
        file_out,
        p_train=[]):
    ids_max = np.argsort(scores)[::-1]
    id_question = m.vocabulary.get_id(p_test_one[0])
 #   print ("p_test=",p_test_one)
    # for i in ids_max[:2]:
    #     if i == id_question: continue
    #     ans=m.vocabulary.get_word_by_id(i)
    #     if ans in p_test_one[1]:
    #         file_out.write("{}\t{}\t{}\t{}\n".format(p_test_one[0],p_test_one[1],ans,"YES"))
    #         cnt_correct+=1
    #         props_experiment={"a":p_test_one[0],"a_prime":p_test_one[1],"ans":ans,"correct":"YES","similarity":score_sim[i],"class_proba":score_reg[i],"method":options["name_method"]}
    #         props_experiment.update(m.props)
    #     else:
    #         props_experiment={"a":p_test_one[0],"a_prime":p_test_one[1],"ans":ans,"correct":"NO","similarity":score_sim[i],"class_proba":score_reg[i],"method":options["name_method"]}
    #         props_experiment.update(m.props)
    #         file_out.write("{}\t{}\t{}\t{}\n".format(p_test_one[0],p_test_one[1],ans,"NO"))
    #     #session.append_vals_to_csv("hits.csv",props_experiment)
    #     break
    if do_top5:
        # result={}
        # result["question"]=p_test_one[0]
        # result["expected answer"]=p_test_one[1]
        # result["answers"]=[]
        # for i in ids_max[:5]:
        #     if i == id_question: continue
        #     ans=m.vocabulary.get_word_by_id(i)
        #     d_ans={"answer":ans,"proba":scores[i],"correct":ans in p_test_one[1]}
        #     result["answers"].append(d_ans)
        # s=json.dumps(result,indent=2)
        # file_out.write (s)
        extr = ""
        if len(p_train) > 0:
            extr = "as {} is to {}".format(p_train[1], p_train[0])
            set_exclude = set([p_train[0]]) | set(p_train[1] ) 
        else:
            set_exclude = {}
        set_exclude.add(p_test_one[0])
        set_exclude = {}

        file_out.write("Q: What is to \t{} {}\n".format(p_test_one[0], extr))
        file_out.write("Expected answer:\t{}\n".format(",".join(p_test_one[1])))
        cnt_reported = 0
        for i in ids_max[:10]:
            #if i == id_question:
            #    continue
            ans = m.vocabulary.get_word_by_id(i)
            if ans in set_exclude:
                continue
            cnt_reported += 1
            if score_sim is None:
                file_out.write(
                    "\tA:sc_ttl: {:.3f}\t{}\t".format(
                        scores[i], ans))
            else:
                file_out.write(
                    "\tA:\tsc_class: {:.2f}\tsc_sim: {:.2f}\tsc_ttl: {:.2f}\t{}\t".format(
                        score_reg[i], score_sim[i], scores[i], ans))
            if ans in p_test_one[1]:
                file_out.write("YES\n")
            else:
                file_out.write("NO\n")
            if cnt_reported > 4:
                break
        file_out.write("\n")
    else:
        for i in ids_max[:2]:
            if i == id_question:
                continue
            ans = m.vocabulary.get_word_by_id(i)
            if ans in p_test_one[1]:
                file_out.write(
                    "{}\t{}\t{}\t{}\n".format(
                        p_test_one[0],
                        p_test_one[1],
                        ans,
                        "YES"))
                cnt_correct += 1
                props_experiment = {
                    "a": p_test_one[0],
                    "a_prime": p_test_one[1],
                    "ans": ans,
                    "correct": "YES",
                    "similarity": score_sim[i],
                    "class_proba": score_reg[i],
                    "method": options["name_method"]}
                props_experiment.update(m.props)
            else:
                props_experiment = {
                    "a": p_test_one[0],
                    "a_prime": p_test_one[1],
                    "ans": ans,
                    "correct": "NO",
                    "similarity": score_sim[i],
                    "class_proba": score_reg[i],
                    "method": options["name_method"]}
                props_experiment.update(m.props)
                file_out.write(
                    "{}\t{}\t{}\t{}\n".format(
                        p_test_one[0],
                        p_test_one[1],
                        ans,
                        "NO"))
            # session.append_vals_to_csv("hits.csv",props_experiment)
            break


def do_test_on_pair_regr_old(p_test, p_train, file_out):
    cnt_total = 0
    cnt_correct = 0
    # create_list_test_right(p_test)

    X_train, Y_train = gen_vec_single(p_train)
    # print(Y_train)
    if options["name_method"].startswith("LRCos"):
        #        model_regression = LogisticRegression(class_weight = 'balanced')
        #model_regression = Pipeline([('poly', PolynomialFeatures(degree=3)), ('logistic', LogisticRegression(class_weight = 'balanced',C=C))])
        model_regression = LogisticRegression(
            class_weight='balanced',
            C=inverse_regularization_strength)
    if options["name_method"] == "SVMCos":
        model_regression = sklearn.svm.SVC(
            kernel=name_kernel,
            cache_size=1000,
            class_weight='balanced',
            probability=True)
    model_regression.fit(X_train, Y_train)
    score_reg = model_regression.predict_proba(m.matrix)[:, 1]
    for p_test_one in p_test:
        cnt_total += 1
        if is_pair_missing(p_test_one):
            # file_out.write("{}\t{}\t{}\n".format(p_test_one[0],p_test_one[1],"MISSING"))
            continue
        v = m.get_row(p_test_one[0])
        v /= np.linalg.norm(v)
        score_sim = v @ m_normed.T
        # scores=score_sim*np.sqrt(score_reg)
        scores = score_sim * score_reg
        process_prediction(p_test_one, scores, score_reg, score_sim, file_out)

    return cnt_total, cnt_correct


def do_test_on_pair_regr(p_test, p_train, file_out):
    cnt_total = 0
    cnt_correct = 0
    # create_list_test_right(p_test)
    X_train, Y_train = gen_vec_single_nonoise(p_train)
    model = sklearn.svm.SVC(kernel="linear", probability=True)
    model.fit(X_train, Y_train)
    cof = abs(model.coef_[0])
    cof = cof / np.max(cof)
    cof = 1 - cof

    X_train, Y_train = gen_vec_single(p_train)
    if options["name_method"] == "LRCosF":
        #        model_regression = LogisticRegression(class_weight = 'balanced')
        #model_regression = Pipeline([('poly', PolynomialFeatures(degree=3)), ('logistic', LogisticRegression(class_weight = 'balanced',C=C))])
        model_regression = LogisticRegression(
            class_weight='balanced',
            C=inverse_regularization_strength)
    if options["name_method"] == "SVMCos":
        model_regression = sklearn.svm.SVC(
            kernel=name_kernel,
            cache_size=1000,
            class_weight='balanced',
            probability=True)
    model_regression.fit(X_train, Y_train)
    score_reg = model_regression.predict_proba(m.matrix)[:, 1]
    for p_test_one in p_test:
        cnt_total += 1
        if is_pair_missing(p_test_one):
            file_out.write(
                "{}\t{}\t{}\n".format(
                    p_test_one[0],
                    p_test_one[1],
                    "MISSING"))
            continue
        v = m.get_row(p_test_one[0])
        v /= np.linalg.norm(v)
        v = v * cof
        score_sim = v @ m_normed.T
        scores = score_sim * score_reg
        process_prediction(p_test_one, scores, score_reg, score_sim, file_out)

    return cnt_total, cnt_correct

#@profile


def do_test_on_pair_3CosAvg(p_test, p_train, file_out):
    cnt_total = 0
    cnt_correct = 0
    vecs_a = []
    vecs_a_prime = []
    for p in p_train:
        vecs_a_prime_local=[]
        for t in p[1]:
            if m.vocabulary.get_id(t) >= 0:
                vecs_a_prime_local.append(m.get_row(t))
            break
        if len(vecs_a_prime_local)>0:
            vecs_a.append(m.get_row(p[0]))
            vecs_a_prime.append(np.vstack(vecs_a_prime_local).mean(axis=0))
    if len(vecs_a_prime) == 0:
        for p_test_one in p_test:
            file_out.write(
                "{}\t{}\t{}\n".format(
                    p_test_one[0],
                    p_test_one[1],
                    "training MISSING"))
        return(len(p_test), 0)

    vec_a = np.vstack(vecs_a).mean(axis=0)
    vec_a_prime = np.vstack(vecs_a_prime).mean(axis=0)

    for p_test_one in p_test:
        cnt_total += 1
        if is_pair_missing(p_test_one):
            #   file_out.write("{}\t{}\t{}\n".format( p_test_one[0], p_test_one[1], "MISSING"))
            continue
        vec_b = m.get_row(p_test_one[0])
        vec_b_prime = vec_a_prime - vec_a + vec_b
        scores = get_most_similar_fast(vec_b_prime)
        process_prediction(p_test_one, scores, None, None, file_out)

        # ids_max=np.argsort(scores)[::-1]
        # id_question = m.vocabulary.get_id(p_test_one[0])
        # for i in ids_max[:2]:
        #     if i == id_question: continue
        #     ans=m.vocabulary.get_word_by_id(i)
        #     if ans in p_test_one[1]:
        #         file_out.write("{}\t{}\t{}\t{}\n".format(p_test_one[0],p_test_one[1],ans,"YES"))
        #         cnt_correct+=1
        #     else:
        #         file_out.write("{}\t{}\t{}\t{}\n".format(p_test_one[0],p_test_one[1],ans,"NO"))
        #     break
    return cnt_total, cnt_correct


do_test_on_pairs = None


def register_test_func():
    global do_test_on_pairs
    if options["name_method"] == "3CosAvg":
        do_test_on_pairs = do_test_on_pair_3CosAvg
    elif options["name_method"] == "3CosAdd":
        do_test_on_pairs = do_test_on_pair_3CosAdd
    elif options["name_method"] == "PairDistance":
        do_test_on_pairs = do_test_on_pair_3CosAdd
    elif options["name_method"] == "LRCos" or options["name_method"] == "SVMCos":
        do_test_on_pairs = do_test_on_pair_regr_old
    elif options["name_method"] == "LRCosF":
        do_test_on_pairs = do_test_on_pair_regr
    else:
        raise Exception("method name not recognized")


def run_category_subsample(pairs, name_dataset, name_category="not yet"):
    name_file_out = os.path.join(
        ".",
        dir_out,
        name_dataset,
        options["name_method"])
    if options["name_method"] == "SVMCos":
        name_file += "_" + name_kernel
    name_file_out += "/" + m.name + "/" + name_category
    print("saving to", name_file_out)
    if not os.path.exists(os.path.dirname(name_file_out)):
        os.makedirs(os.path.dirname(name_file_out))
    file_out = open(name_file_out, "w", errors="replace")
    file_out.close()


def run_category(pairs, name_dataset, name_category="not yet"):
    global cnt_total_total
    global cnt_total_correct
    name_file_out = os.path.join(
        ".",
        dir_out,
        name_dataset,
        options["name_method"])
    if options["name_method"] == "SVMCos":
        name_file_out += "_" + name_kernel
    if options["name_method"].startswith("LRCos"):
        name_file_out += "_C{}".format(inverse_regularization_strength)
    name_file_out += "/" + m.name + "/" + name_category
    print("saving to", name_file_out)
    if not os.path.exists(os.path.dirname(name_file_out)):
        os.makedirs(os.path.dirname(name_file_out))
    #loo = sklearn.cross_validation.LeaveOneOut(len(pairs))
    kf = sklearn.model_selection.KFold(n_splits=len(pairs) // size_cv_test)
    cnt_splits=kf.get_n_splits(pairs)
    loo = kf.split(pairs)
    if need_subsample:
        file_out = open("/dev/null", "a", errors="replace")
        loo = sklearn.cross_validation.KFold(
            n=len(pairs), n_folds=len(pairs) // size_cv_test)
        for max_size_train in range(10, 300, 5):
            finished = False
            my_prog = tqdm(
                0,
                total=len(loo),
                desc=name_category +
                ":" +
                str(max_size_train))
            cnt_total = 0
            cnt_correct = 0
            for train, test in loo:
                p_test = [pairs[i] for i in test]
                p_train = [pairs[i] for i in train]
                p_train = [x for x in p_train if not is_pair_missing(x)]
                if len(p_train) <= max_size_train:
                    finished = True
                    continue
                p_train = random.sample(p_train, max_size_train)
                my_prog.update()
                t, c = do_test_on_pairs(p_test, p_train, file_out)
                cnt_total += t
                cnt_correct += c
            if finished:
                print("finished")
                break
            props_experiment = {
                "vectors": m.name,
                "dataset": name_dataset,
                "method": options["name_method"],
                "category": name_category,
                "total": cnt_total,
                "correct": cnt_correct,
                "size_train": max_size_train}
            props_experiment.update(m.props)
            # session.append_vals_to_csv("subsample.csv",props_experiment)
            # session.flush()
        cnt_total_total += cnt_total
        cnt_total_correct += cnt_correct
    else:
        file_out = open(name_file_out, "w", errors="replace")
        my_prog = tqdm(0, total=cnt_splits, desc=name_category)
        cnt_total = 0
        cnt_correct = 0
        for train, test in loo:
            p_test = [pairs[i] for i in test]
            p_train = [pairs[i] for i in train]
            p_train = [x for x in p_train if not is_pair_missing(x)]
            my_prog.update()
            t, c = do_test_on_pairs(p_test, p_train, file_out)
            cnt_total += t
            cnt_total_total += t
            cnt_correct += c
            cnt_total_correct += c
        props_experiment = {
            "vectors": m.name,
            "dataset": name_dataset,
            "method": options["name_method"],
            "category": name_category,
            "total": cnt_total,
            "correct": cnt_correct}
        props_experiment.update(m.props)
        # session.append_vals_to_csv("acc.csv",props_experiment)
    file_out.close()
    # session.flush()


def get_pairs(fname):
    pairs = []
    with open(fname) as f:
        id_line = 0
        for line in f:
            try:
                id_line += 1
                if "\t" in line:
                    left, right = line.lower().split("\t")
                else:
                    left, right = line.lower().split()
                right = right.strip()
                if "/" in right:
                    right = [i.strip() for i in right.split("/")]
                else:
                    right = [i.strip() for i in right.split(",")]
                pairs.append([left, right])
            except:
                print("error reading pairs")
                print("in file", fname)
                print("in line", id_line, line)
                exit(-1)

    return pairs


def run_all(name_dataset):
    global cnt_total_correct
    global cnt_total_total
    register_test_func()
    cnt_total_correct = 0
    cnt_total_total = 0
    print("doing all for ", name_dataset)
    if options["name_method"] == "SVMCos":
        print("using ", options["name_method"] + "_" + name_kernel)
    else:
        print("using ", options["name_method"])
    dir_tests = os.path.join(options["dir_root_dataset"], name_dataset)
    if not os.path.exists(dir_tests):
        raise Exception("test dataset dir does not exist")
    for root, dirnames, filenames in os.walk(dir_tests):
        for filename in fnmatch.filter(sorted(filenames), '*'):
            print(filename)
            pairs = get_pairs(os.path.join(root, filename))
            # print(pairs)
            run_category(pairs, name_dataset, name_category=filename)
    #print("total accuracy: {:.4f}".format(cnt_total_correct/(cnt_total_total+1)))


def subsample_dims(newdim):
    m.matrix = m.matrix[:, 0:newdim]
    m.name = re.sub("_d(\d+)", "_d{}".format(newdim), m.name)


def make_normalized_copy():
    global m_normed
    m_normed = m.matrix.copy()
    print("created matrix copy for normalization, normalizing.... ")
    # print(type(m_normed))
    if scipy.sparse.issparse(m_normed):
        norm = scipy.sparse.linalg.norm(m_normed, axis=1)[:, None]
        m_normed.data /= norm.repeat(np.diff(m_normed.indptr))
    else:
        m_normed /= np.linalg.norm(m_normed, axis=1)[:, None]

    print("normalized copy")


#    for dims in [1300,1200,1000,900,800,700,600,500,400,300,200,100]:
#    for dims in [1000,800,600,400,300,200]:
#        subsample_dims(dims)
#        make_normalized_copy()
#        run_all("BATS2.0")

# for d in dirs:
#    for alpha in [0.2,0.4,0.6,0.8,1.0]:
    # for alpha in [0.1,0.2,0.4,0.6,0.8,1.0]:
    #   m = vsmlib.model.Model_numbered()
#        m.load_with_alpha("/home/blackbird/data/scratch/explicit/English/_factorized/explicit_combined2_m100_w5_svd_d2000",alpha)
    #  m.load_with_alpha("/home/blackbird/data/scratch/explicit/English/_factorized/explicit_combined2_m100_w5_svd_d2000",alpha)
    # m.normalize()
    #m_normed =  m.matrix.copy()
    # m_normed/=np.linalg.norm(m_normed,axis=1)[:,None]

    # subsample_dims(dims)
    # make_normalized_copy()
    # run_all("BATS2.0")


def main():
    # chech args and print error if needed
    global options
    #print("here we go!")
#    ParseOptions()
    if len(sys.argv) > 1:
        path_config = sys.argv[1]
    else:
        path_config = "config_sample.yaml"

        #print ("config file name required")
        # exit()

    with open(path_config, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    print(cfg)
    dirs = cfg["path_vectors"]
    options["name_method"] = cfg["method"]
    # return
    # check if all pathes exist
    options["path_dataset"] = cfg["path_dataset"]
    options["name_dataset"] = os.path.basename(options["path_dataset"])
    options["dir_root_dataset"] = os.path.dirname(options["path_dataset"])

    global m
    for d in dirs:
        if "factorized" in d:
            alpha = cfg["alpha"]
            m = vsmlib.model.Model_numbered()
            m.load_with_alpha(d, alpha)
        else:
            m = vsmlib.model.load_from_dir(d)

        if m.name.startswith("explicit"):
            # m.clip_negatives()  #make this configurable
            m.normalize()
        print(m.name)
        name_model = m.name
        make_normalized_copy()

        run_all(options["name_dataset"])


if __name__ == "__main__":
    main()


# m2=vsmlib.model.load_from_dir("/home/blackbird/data/scratch/sparse/English/_converted/explicit_combined2_m100_w2_svd_1000_C0.6/")
# m2.normalize()
# m.matrix=np.hstack([m.matrix,m2.matrix])
# m.name+=m2.name
