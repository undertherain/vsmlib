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
from itertools import product

def profile_trivial(a):
    return a
try:
    profile
except NameError:
    profile = profile_trivial


options = {}

do_top5 = True

normalize=True

# this are some hard-coded bits which will be implemented later
need_subsample = False
size_cv_test = 1
set_aprimes_test = None
inverse_regularization_strength = 1.0

result_miss = {
    "rank": -1,
    "reason": "missing words"
    }

# options["degree"]=3
# name_method="SVMCos"
# name_kernel="linear"
# name_kernel="poly"
# name_kernel='rbf'


def normed(v):
    if normalize:
        return v
    else:
        return v / np.linalg.norm(v)


def get_most_similar_fast(v):
    scores = normed(v) @ m_normed.T
    scores = (scores + 1) / 2
    return scores



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


def is_at_least_one_word_present(words):
    for w in words:
        if m.vocabulary.get_id(w) >= 0:
            return True
    return False


def is_pair_missing(pairs):
    for pair in pairs:
        if m.vocabulary.get_id(pair[0]) < 0:
            return True
        if m.vocabulary.get_id(pair[1][0]) < 0:
            return True
        #if not is_at_least_one_word_present(pair[1]):
            #return True
    return False


#def is_quad_missing(quad):
#    if m.vocabulary.get_id(quad[0]) < 0:
#        return True
#    if m.vocabulary.get_id(quad[2]) < 0:
#        return True
#    if m.vocabulary.get_id(quad[1][0]) < 0:
#        return True
#    if m.vocabulary.get_id(quad[3][0]) < 0:
#        return True
#    return False


def gen_vec_single(pairs):
    a, a_prime = zip(*pairs)
    a_prime = [i[0] for i in a_prime]
    #a_prime=[i for sublist in a_prime for i in sublist]
    a_prime = [i for i in a_prime if m.vocabulary.get_id(i) >= 0]
    a = [i for i in a if m.vocabulary.get_id(i) >= 0]
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


def get_crowndedness(vector):
    scores = get_most_similar_fast(vector)
    scores.sort()
    return (scores[-11:-1][::-1]).tolist()


class PairWise:
    def __call__(self, pairs_train, pairs_test):
        results = []
        for p_train, p_test in product(pairs_train, pairs_test):
            if is_pair_missing([p_train, p_test]):
                continue
            result = self.do_on_two_pairs(p_train, p_test)
            result["b in neighbourhood of b_prime"] = get_rank(p_test[0], p_test[1][0])
            result["b_prime in neighbourhood of b"] = get_rank(p_test[1], p_test[0])
            results.append(result)
        return results

    def do_on_two_pairs(self, p_train, p_test):
        vec_a = m.get_row(p_train[0])
        vec_a_prime = m.get_row(p_train[1][0])
        vec_b = m.get_row(p_test[0])
        vec_b_prime = m.get_row(p_test[1][0])
        if scipy.sparse.issparse(m.matrix):
            vec_a = vec_a.toarray()[0]
            vec_a_prime = vec_a_prime.toarray()[0]
            vec_b = vec_b.toarray()[0]

        scores, vec_b_prime_predicted = self.compute_scores(vec_a, vec_a_prime, vec_b)
        ids_max = np.argsort(scores)[::-1]
        result = process_prediction(p_test, scores, None, None, [p_train], exclude=options["exclude"])
        self.collect_stats(result, vec_a, vec_a_prime, vec_b, vec_b_prime, vec_b_prime_predicted)
        return result

    def collect_stats(self, result, vec_a, vec_a_prime, vec_b, vec_b_prime, vec_b_prime_predicted):
        if not vec_b_prime_predicted is None:
            result["similarity predicted to b_prime cosine"]=m.cmp_vectors(vec_b_prime_predicted, vec_b_prime)
        
        result["similarity a to a_prime cosine"]=m.cmp_vectors(vec_a, vec_a_prime)
        result["similarity a_prime to b_prime cosine"]=m.cmp_vectors(vec_a_prime, vec_b_prime)
        result["similarity b to b_prime cosine"]=m.cmp_vectors(vec_b, vec_b_prime)
        result["similarity a to b_prime cosine"]=m.cmp_vectors(vec_a, vec_b_prime)
        
        result["distance a to a_prime euclidean"] = scipy.spatial.distance.euclidean(vec_a, vec_a_prime)
        result["distance a_prime to b_prime euclidean"] = scipy.spatial.distance.euclidean(vec_a_prime, vec_b_prime)
        result["distance b to b_prime euclidean"] = scipy.spatial.distance.euclidean(vec_b, vec_b_prime)
        result["distance a to b_prime euclidean"] = scipy.spatial.distance.euclidean(vec_a, vec_b_prime)
        
        result["crowdedness of b_prime"] = get_crowndedness(vec_b_prime)


class LinearOffset(PairWise):
    def compute_scores(self, vec_a, vec_a_prime, vec_b):
        vec_b_prime_predicted = vec_a_prime - vec_a + vec_b
        vec_b_prime_predicted = normed(vec_b_prime_predicted)
        scores = get_most_similar_fast(vec_b_prime_predicted)
        return scores, vec_b_prime_predicted


class PairDistance(PairWise):
    def compute_scores(self, vec_a, vec_a_prime, vec_b):
        scores = get_most_collinear_fast(vec_a, vec_a_prime, vec_b)
        return scores, vec_b_prime_predicted


class ThreeCosMul(PairWise):
    def compute_scores(self, vec_a, vec_a_prime, vec_b):
        epsilon = 0.001
        sim_a = get_most_similar_fast(vec_a)
        sim_a_prime = get_most_similar_fast(vec_a_prime)
        sim_b = get_most_similar_fast(vec_b)
        scores = (sim_a_prime * sim_b) / (sim_a + epsilon)
        return scores, None


class ThreeCosMul2(PairWise):
    def compute_scores(self, vec_a, vec_a_prime, vec_b):
        epsilon = 0.001
        #sim_a = get_most_similar_fast(vec_a)
        #sim_a_prime = get_most_similar_fast(vec_a_prime)
        #sim_b = get_most_similar_fast(vec_b)
        #   scores = (sim_a_prime * sim_b) / (sim_a + epsilon)
        predicted = ( ((vec_a_prime+0.5) /2) * ((vec_b+0.5)/2)) / (((vec_a+0.5)/2) + epsilon)
        scores = get_most_similar_fast(predicted)
        return scores, predicted

class SimilarToAny(PairWise):
    def compute_scores(self, vectors):
        scores = get_most_similar_fast(vectors)
        #print("scores shape:", scores.shape)
        best = scores.max(axis=0)
        return best


class SimilarToB():
    def __call__(self, pairs_train, pairs_test):
        results=[]
        for p_test in  pairs_test:
            if is_pair_missing([p_test]): continue
            result = self.do_on_two_pairs(p_test)
            result["b in neighbourhood of b_prime"] = get_rank(p_test[0],p_test[1][0])
            result["b_prime in neighbourhood of b"] = get_rank(p_test[1],p_test[0])
            results.append(result)
        return results

    def do_on_two_pairs(self, pair_test):
        #print ("pre ",pair_test)
        if is_pair_missing([pair_test]):
            result=result_miss
        else:
            vec_b = m.get_row(pair_test[0])
            vec_b_prime = m.get_row(pair_test[1][0])
            scores = get_most_similar_fast(vec_b)
            result = process_prediction(pair_test, scores, None, None)
            result["similarity to correct cosine"]=m.cmp_vectors(vec_b,vec_b_prime)
        return result
   

def do_test_on_pair_3CosAvg(p_train, p_test):
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
        print("AAAA SOMETHIGN MISSING")
        return([])

    vec_a = np.vstack(vecs_a).mean(axis=0)
    vec_a_prime = np.vstack(vecs_a_prime).mean(axis=0)

    results=[]
    for p_test_one in p_test:
        if is_pair_missing(p_test_one):
            continue
        vec_b_prime = m.get_row(p_test_one[1][0])
        vec_b = m.get_row(p_test_one[0])
        vec_b_prime_predicted = vec_a_prime - vec_a + vec_b
        # oh crap, why are we not normalizing here? 
        scores = get_most_similar_fast(vec_b_prime_predicted)
        result = process_prediction(p_test_one, scores, None, None)
        result["distances to correct cosine"]=m.cmp_vectors(vec_b_prime_predicted,vec_b_prime)
        results.append(result)
    return results


def create_list_test_right(pairs):
    global set_aprimes_test
    a, a_prime = zip(*pairs)
    a_prime = [i for sublist in a_prime for i in sublist]
    set_aprimes_test = set(a_prime)

def get_distance_closest_words(center,cnt_words=1):
    scores = get_most_similar_fast(center)
    ids_max = np.argsort(scores)[::-1]
    distances = np.zeros(cnt_words)
    for i in range(cnt_words):
        distances[i] = scores[ids_max[i+1]]
    return distances.mean()

def get_rank(source,center):
    if isinstance(center, str):
        #print ("getting rank for ",center)
        center = m.get_row(center)
    if isinstance(source, str):
        source = [source]
    scores = get_most_similar_fast(center)
    ids_max = np.argsort(scores)[::-1]
    for i in range(ids_max.shape[0]):
        #print("\t try ", m.vocabulary.get_word_by_id(ids_max[i]))
        if m.vocabulary.get_word_by_id(ids_max[i]) in source: break
    rank = i
    return rank

def process_prediction(p_test_one, scores, score_reg, score_sim, p_train=[], exclude=True):
    ids_max = np.argsort(scores)[::-1]
    id_question = m.vocabulary.get_id(p_test_one[0])
    result = dict()
    cnt_answers_to_report=6
    extr = ""
    if len(p_train) == 1:
        extr = "as {} is to {}".format(p_train[0][1], p_train[0][0])
        set_exclude = set([p_train[0][0]]) | set(p_train[0][1] ) 
    else:
        set_exclude = set()
    set_exclude.add(p_test_one[0])
    result["question verbose"] = "What is to {} {}".format(p_test_one[0], extr)
    result["b"] = p_test_one[0]
    result["expected answer"] = p_test_one[1]
    result["predictions"] = []
    cnt_reported = 0
    for i in ids_max[:10]:
        prediction = dict()
        ans = m.vocabulary.get_word_by_id(i)
        if exclude and (ans in set_exclude):
            continue
        cnt_reported += 1
        prediction["score"]=float(scores[i])
        prediction["answer"]=ans
        if ans in p_test_one[1]:
            prediction["hit"]=True
        else:
            prediction["hit"]=False
        result["predictions"].append(prediction)
        if cnt_reported >= cnt_answers_to_report:
            break
    rank = 0
    for i in range(ids_max.shape[0]):
        ans = m.vocabulary.get_word_by_id(ids_max[i])
        if exclude and (ans in set_exclude):
            continue
        if ans in p_test_one[1]: break
        rank+=1
    result["rank"] = rank
 
    #vec_b_prime = m.get_row(p_test_one[1][0])
    #result["closest words to answer 1"] = get_distance_closest_words(vec_b_prime,1)
    #result["closest words to answer 5"] = get_distance_closest_words(vec_b_prime,5)
    #where prediction lands:
    ans = m.vocabulary.get_word_by_id(ids_max[0])
    if ans == p_test_one[0]: 
        result["landing_b"]=True 
    else:
        result["landing_b"]=False 

    if ans in p_test_one[1]: 
        result["landing_b_prime"]=True 
    else:
        result["landing_b_prime"]=False 

    all_a = [i[0] for i in p_train]

    all_a_prime = [item for sublist in p_train for item in sublist[1]]
#    print("all_a",all_a)
    #print("all_a_prime",all_a_prime)
    if ans in all_a: 
        result["landing_a"]=True 
    else:
        result["landing_a"]=False 

    if ans in all_a_prime: 
        result["landing_a_prime"]=True 
    else:
        result["landing_a_prime"]=False 

    return result


def do_test_on_pair_regr_old(p_train, p_test):
    results = []
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
        if is_pair_missing([p_test_one]):
            # file_out.write("{}\t{}\t{}\n".format(p_test_one[0],p_test_one[1],"MISSING"))
            continue
        vec_b = m.get_row(p_test_one[0])
        vec_b_prime = m.get_row(p_test_one[1][0])
        v = vec_b / np.linalg.norm(vec_b)
        score_sim = v @ m_normed.T
        # scores=score_sim*np.sqrt(score_reg)
        scores = score_sim * score_reg
        result = process_prediction(p_test_one, scores, score_reg, score_sim)
        result["similarity b to b_prime cosine"]=m.cmp_vectors(vec_b, vec_b_prime)
        results.append(result)
    return results


def do_test_on_pair_regr(p_train, p_test, file_out):
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


do_test_on_pairs = None

def register_test_func():
    global do_test_on_pairs
    if options["name_method"] == "3CosAvg":
        do_test_on_pairs = do_test_on_pair_3CosAvg
    elif options["name_method"] == "SimilarToAny":
        do_test_on_pairs = SimilarToAny()
    elif options["name_method"] == "SimilarToB":
        do_test_on_pairs = SimilarToB()
    elif options["name_method"] == "3CosMul":
        do_test_on_pairs = ThreeCosMul()
    elif options["name_method"] == "3CosMul2":
        do_test_on_pairs = ThreeCosMul2()
    elif options["name_method"] == "3CosAdd":
        do_test_on_pairs = LinearOffset()
    elif options["name_method"] == "PairDistance":
        do_test_on_pairs = PairDistance()
    elif options["name_method"] == "LRCos" or options["name_method"] == "SVMCos":
        do_test_on_pairs = do_test_on_pair_regr_old
    elif options["name_method"] == "LRCosF":
        do_test_on_pairs = do_test_on_pair_regr
    else:
        raise Exception("method name not recognized")


def run_category_subsample(pairs, name_dataset, name_category="not yet"):
    name_file_out = os.path.join(
        ".",
        options["path_results"],
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

    if name_dataset.endswith("_D") or name_dataset.endswith("_I") or name_dataset.endswith("_E") or name_dataset.endswith("_L"):
        name_dataset = name_dataset[:-2]

    results = []
    name_file_out = os.path.join(options["path_results"], name_dataset, options["name_method"])
    if options["name_method"] == "SVMCos":
        name_file_out += "_" + name_kernel
    if options["name_method"].startswith("LRCos"):
        name_file_out += "_C{}".format(inverse_regularization_strength)
    if not options["exclude"]:
        name_file_out += "_honest"
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
            my_prog = tqdm(0, total=len(loo), desc=name_category + ":" + str(max_size_train))
            for train, test in loo:
                p_test = [pairs[i] for i in test]
                p_train = [pairs[i] for i in train]
                p_train = [x for x in p_train if not is_pair_missing(x)]
                if len(p_train) <= max_size_train:
                    finished = True
                    continue
                p_train = random.sample(p_train, max_size_train)
                my_prog.update()
                do_test_on_pairs(p_train, p_test, file_out)
            if finished:
                print("finished")
                break

    else:
        my_prog = tqdm(0, total=cnt_splits, desc=name_category)
        cnt_total = 0
        cnt_correct = 0
        for train, test in loo:
            p_test = [pairs[i] for i in test]
            p_train = [pairs[i] for i in train]
            #p_train = [x for x in p_train if not is_pair_missing(x)]
            my_prog.update()
            results += do_test_on_pairs(p_train, p_test)

        props_experiment = {
            "vectors": m.name,
            "dataset": name_dataset,
            "method": options["name_method"],
            "category": name_category,
            "total": cnt_total,
            "correct": cnt_correct}
        props_experiment.update(m.props)
    out = dict()
    out["results"]=results
    out["experiment setup"]=dict()
    out["experiment setup"]["method"] = options["name_method"]
    if not options["exclude"]:
        out["experiment setup"]["method"] += "_honest"
    out["experiment setup"]["dataset"] = name_dataset
    out["experiment setup"]["embeddings"] = m.name
    out["experiment setup"]["category"] = name_category
    str_results = json.dumps(out, indent=4, separators=(',', ': '), sort_keys=True)
    #print(str_results) 
    file_out = open(name_file_out, "w", errors="replace")
    file_out.write(str_results)
    file_out.close()
    

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
    if normalize:
        m_normed = m.matrix
    else:
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
    options["exclude"] = cfg["exclude"]
    # return
    # check if all pathes exist
    options["path_dataset"] = cfg["path_dataset"]
    options["name_dataset"] = os.path.basename(options["path_dataset"])


    options["dir_root_dataset"] = os.path.dirname(options["path_dataset"])
    options["path_results"] = cfg["path_results"]
    global m
    for d in dirs:
        if "factorized" in d:
            alpha = cfg["alpha"]
            m = vsmlib.model.Model_numbered()
            m.load_with_alpha(d, alpha)
        else:
            m = vsmlib.model.load_from_dir(d)

        if normalize:
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