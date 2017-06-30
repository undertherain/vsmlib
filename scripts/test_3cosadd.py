import numpy as np
import os
import sys
import pandas
sys.path.append("/work/alex/projects/NLP/vsmlib/")
import vsmlib
import sklearn
import sklearn.model_selection
import fnmatch
from tqdm import tqdm

#path_vectors="/work/alex/data/linguistic/vectors/glove/6b.wiki_giga"
path_vectors="/work/alex/data/linguistic/vectors/explicit/English/_converted/explicit_combined2_m100_w3_svd_d1000_a1"
#path_vectors="/work/alex/data/linguistic/vectors/explicit/English/_converted/explicit_BNC_m100_w2_svd_200_C1"  

#dir_tests="/work/alex/data/linguistic/datasets/analogies/BATS_3.0/1_Inflectional_morphology/"
#dir_tests="/work/alex/data/linguistic/datasets/analogies/BATS_3.0/2_Derivational_morphology"
#dir_tests="/work/alex/data/linguistic/datasets/analogies/BATS_3.0/3_Encyclopedic_semantics"
#dir_tests="/work/alex/data/linguistic/datasets/analogies/BATS_3.0/4_Lexicographic_semantics"

#dir_tests="/work/alex/data/linguistic/datasets/analogies/Google"
dir_tests="/work/alex/data/linguistic/datasets/analogies/BATS_3.0"

name_dataset=dir_tests.split("/")[-1]

m=vsmlib.model.load_from_dir(path_vectors)
m.normalize()

path_out="/work/alex/data/linguistic/outputs/csv"
path_out = os.path.join(path_out,name_dataset,m.name)
print(path_out)
#path_out="./out_csv"
if not os.path.exists(path_out):
    os.makedirs(path_out)


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

def get_argmax_filtered(scores,exclude_set):
    ids=np.argsort(scores)[::-1]
    for i in range(len(exclude_set)+1):
        word=m.vocabulary.get_word_by_id(ids[i])
        if word in exclude_set: continue
        return word

def get_rank(scores,target_words):
    ids=np.argsort(scores)[::-1]
    for i in range(scores.shape[0]):
        if m.vocabulary.get_word_by_id(ids[i]) in target_words:
            return i+1
    return 0
        
def do_on_pair(p_train,p_test):
    if is_quad_missing(p_train + p_test): return
    #print (p_train,p_test)
    a=p_train[0]
    a_prime=p_train[1]
    b=p_test[0]
    dic_quad={"a":a,"a_prime":a_prime,"b":b,"expected_b_prime":p_test[1]}
    vec_a = m.get_row(a)
    vec_a_prime = m.get_row(a_prime[0])
    vec_b = m.get_row(b)
    vec_b_prime = vec_a_prime - vec_a + vec_b
    vec_b_prime /= np.linalg.norm(vec_b_prime)
    error_distance=m.cmp_vectors(vec_b_prime,m.get_row(p_test[1][0]))
    vectors=np.vstack([vec_a,vec_a_prime,vec_b,vec_b_prime])
    scores = m.matrix @ vectors.T
    scores = scores.T
    #print (scores.shape)
    answer_honest=m.vocabulary.get_word_by_id(np.argmax(scores[3]))
    dic_quad["answer_honest"]=answer_honest
    dic_quad["rank_honest"]=get_rank(scores[3],p_test[1])
    set_exclude = set([p_train[0]]) | set(p_train[1]) | set([p_test[0]])
    dic_quad["answer_filtered"]=get_argmax_filtered(scores[3],set_exclude)
    dic_quad["close_to_a"]=get_argmax_filtered(scores[0],set_exclude)
    dic_quad["close_to_a_prime"]=get_argmax_filtered(scores[1],set_exclude)
    dic_quad["close_to_b"]=get_argmax_filtered(scores[2],set_exclude)
    dic_quad["error_distance"]=error_distance
    lst_quads.append(dic_quad)

def do_on_file(fname):
    global lst_quads
    pairs = get_pairs(fname)
    name_category=os.path.basename(fname).replace(".txt","")
    lst_quads=[]

    loo = sklearn.model_selection.LeaveOneOut()
    cnt_splits=loo.get_n_splits(pairs)
    my_prog = tqdm(0, total=cnt_splits, desc=name_category)
        
    for train_index, test_index in loo.split(pairs):
        my_prog.update()
        #print("TRAIN:", train_index, "TEST:", test_index)
        ps_train = [pairs[i] for i in train_index]
        p_test  = [pairs[i] for i in test_index][0]
        for p_train in ps_train:
            do_on_pair(p_train,p_test)
        #break
    #break
    df=pandas.DataFrame(lst_quads,columns=["a","a_prime","b","expected_b_prime","answer_filtered","answer_honest","close_to_a","close_to_a_prime","close_to_b","error_distance","rank_honest"])
    df.to_csv(os.path.join(path_out,name_category+".csv"),index=False)
    #y_train, y_test = y[train_index], y[test_index]
    #print(X_train, X

for root, dirnames, filenames in os.walk(dir_tests):
        for filename in fnmatch.filter(sorted(filenames), '*'):
            do_on_file(os.path.join(root,filename))

