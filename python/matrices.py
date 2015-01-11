# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os
import socket
import time
import numpy as np
import scipy
from scipy import sparse
import sklearn
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
from IPython.display import HTML
import matplotlib as mpl
from matplotlib import pyplot as plt
import math
import glob
import vsmlib
from vsmlib import testhelper,matrix

if socket.gethostname()=="cypress":  dir_root="/storage/scratch/BNC"
if socket.gethostname()=="ashtree":  dir_root="/mnt/work/nlp_scratch/small"
if socket.gethostname()=="rc017.m.gsic.titech.ac.jp":  dir_root="/home/blackbird/data/scratch/brown"

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def countof_fmt(num, suffix=''):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1000.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

# <codecell>

dic_words_ids={}
f=open(os.path.join(dir_root,"ids"), encoding='utf-8', errors='replace')
lines=f.readlines()
for line in lines:
    tokens=line.split()
    dic_words_ids[tokens[0]]=int(tokens[1])
f.close()

lst_words=[]
lst_words=lst_words+([i[0] for i in sorted(dic_words_ids.items(), key=lambda x: x[1])])

def get_id(w):
    try:
        return dic_words_ids[w]
    except :
        return -1
    
def get_word_by_id(i):
    return(lst_words[i])

# <codecell>

cooccurrence=matrix.load_matrix_csr(dir_root,dic_words_ids,zero_negatives=True)
matrix.print_stats(cooccurrence)

#
#sreate sub_matrix
words_of_interest_initial=["day","running","quick","fast","kind","good"]
words_of_interest=[w for w in words_of_interest_initial if w in dic_words_ids]

ids_of_interest=[get_id(w) for w in words_of_interest]
#ids_of_interest
max_width=20

def filter_rows(m):
    xdim=m.shape[1]
    width=min(xdim,max_width)
    #return (cooccurrence[1].todense()[:width])

    dense=np.empty([0,width])
    for i in ids_of_interest:
        if i<0: continue
        if scipy.sparse.issparse(m):
            row=m[i].todense()
        else:
            row=m[i]
        row = np.asarray(row)
        row = np.reshape(row,(xdim))
        dense=np.vstack([dense,row[:width]])
    return (dense)
words_of_interest

# <codecell>

get_id("day")
#print (cooccurrence.shape)
#filter_rows(cooccurrence)
#print (projected.shape)
#filter_rows(cooccurrence)
#m=projected
#width=min(projected.shape[1],max_width)
#dense=np.empty([0, width])
#m[1][:width]
#dense=np.vstack([dense,m[1][:,:width]])

# <codecell>

def get_pmi_v(s):
    values=[]
    idxs=s.nonzero()[1]
    for i in idxs:
        values.append([get_word_by_id(i), s[0,i]])
    values.sort(key=lambda tup: tup[1],reverse=True)
    return values

def get_pmi(w):
    id_w=get_id(w)
    if id_w<0: return []
    #print("id = ",id_w)
    s=cooccurrence[id_w,:]
    return get_pmi_v(s)

def cmp_rows(id1,id2,m=cooccurrence):
    if sparse.issparse(m):
        r1=m[id1].todense()
        r2=m[id2].todense()
        c= cosine(r1,r2)
        if math.isnan(c): return 0
        #c= r1.dot(r2.T)/(np.linalg.norm(r1.data)*np.linalg.norm(r2.data))
        #c= c[0,0]
        return 1- c
    else:
        r1=m[id1,:]
        r2=m[id2,:]
        c= cosine(r1,r2)
        if math.isnan(c): return 0
        return 1-c

    
def cmp_words(w1,w2,m=cooccurrence):
    id1=get_id(w1);
    id2=get_id(w2);
    if (id1<0) or (id2<0): return 0;
    return cmp_rows(id1,id2,m)

#print (cmp_words("day","morning"))

def cmp_first_tail(l,verbose=False):
    max_score=-1;
    max_element=None
    scores=[]
    if verbose: 
        print (l[0]," vs")
    for i in l[1:]:
        score=cmp_words(l[0],i)
        scores.append(score)
        if verbose: print (i.ljust(10)+"\t"+str(score))
    confidence = sorted(scores)[-1]-sorted(scores)[-2]
    return scores,  l[scores.index(max(scores))+1]
    #return l[scores.index(max(scores))+1], confidence

# <codecell>

def get_most_related_words(word):
    scores=[]
    id = get_id(word)
    if id<0: return []
    for i in range(cooccurrence.shape[0]):
        if i==id: continue
        scores.append([cmp_rows(id,i),i])
    scores.sort()
    result=[]
    for q in reversed(scores[-10:]):
        result.append([get_word_by_id(q[1]),q[0]])
    return result


def do_synonyms_test(lines):
    output=""
    cnt_all=0;
    cnt_correct=0;
    lst_conf=[]
    for tokens in lines:
        print ("processing",tokens[0])
        #guess,confidence=cmp_first_tail(tokens[:-1],verbose=False)
        scores,guess=cmp_first_tail(tokens[:-1],verbose=False)
        #print (scores)
        if guess==tokens[-1]:
            cnt_correct+=1
            #lst_conf.append(confidence)
        cnt_all+=1
        #print (tokens[0],guess,guess==tokens[-1],"\n")
        output+="<b>"+tokens[0]+"</b> : "
        for i in range(len(tokens)-2):
            t=tokens[i+1]
            if t==guess:
                if (t==tokens[-1]):
                    output+=" <span style=\"color:green;\">"+t+"</span>"
                else:
                    output+=" <span style=\"color:red;\">"+t+"</span>"
            else: 
                if (t==tokens[-1]):
                    output+=" <span style=\"text-decoration: underline; border-decoration-color: green; -moz-text-decoration-color: green;\">"+t+"</span>"
                else:
                    output+=" "+t
            output+="({:.2f})".format(scores[i])
        output+="</br>\n"
        related=get_most_related_words(tokens[0])
        for r in related:
            output+="{}({:.2f}) ".format(r[0],r[1])
        #if (guess==tokens[-1]):
#            output+="<span style=\"color:green\">correct!</span>"
#        else:
#            output+="<span style=\"color:red\">wrong</span>, should be "+tokens[-1]
        output+="</br>\n"
    success_rate=cnt_correct/cnt_all
    output+="</br>success rate = " + str( success_rate)+"</br>\n"
    #output+="avg confidence = "+ str( np.mean(lst_conf))+"</br>\n"
    with open("last_test.html", 'w') as f:
        print(output,file=f)
    #s_ev.tofile(f)
    return HTML(output)
#do_synonyms_test(testhelper.get_test_from_toefl("../tests/toefl/toefl"))

# <codecell>

#do_synonyms_test(get_test_from_file("../tests/syn_easy.txt"))
do_synonyms_test(testhelper.get_test_from_toefl("../tests/toefl/toefl"))

