import math
import os
import os.path
import copy 
import itertools
import fnmatch
import shutil
import nltk
#import marisa

from collections import OrderedDict
from subprocess import call,Popen,PIPE

class CollocationMeasures(object):
    def raw_frequency(w):
        cache_cfd(w)
        result=nltk.FreqDist()
        cfd=get_cfd(w)
        wc=get_word_count()
        for key in cfd:
            result[key]=(cfd[key]/wc)
        return result
    def pmi(w):
        cache_cfd_pmi(w)
        return cfd_pmi[w]

collocation_measure = None
PREFETCH_INDIVIDUAL_WORDS = False

def dump_list_to_file(filename,lst):
    f = open(filename,"w")
    for i in lst:
        f.write(str(i))
        f.write("\n")
    f.close()    

def my_call(launch_params,**kwargs):
    p = Popen(launch_params,stdout=PIPE,stderr=PIPE,cwd="../preprocess")
    output=p.communicate()
#    print(launch_params)
    if p.wait() != 0:
        print ("There were some errors")
        print (output[1])
        raise BaseException()
    #   print ("out:",output[0])

def check_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def purge():
    for entry in os.listdir(dir_cache):
        full = os.path.join(dir_cache,entry)
        if os.path.isdir(full): shutil.rmtree(full)
        if os.path.isfile(full): os.remove(full)

#def clean(lst):
    #for s in lst:
     #   s.replace("/","_")


path_corpus = ''
dir_cache = ''
cnt_words=0

frequencies=nltk.FreqDist()
cfd = nltk.ConditionalFreqDist()
cfd_pmi = nltk.ConditionalFreqDist()
    
########################### bigrams    ###########################################
def get_cfd(w):
    cache_cfd(w)
    #if now w in cfd: cfd[w]=nltk.ConditionalFreqDist()
    return cfd[w]

def cache_cfd_pmi(w):
    if w in cfd_pmi: return
    cache_cfd(w)
    cfd_pmi[w]=copy.deepcopy(cfd[w])
    pmi=cfd_pmi[w]
    #lst_prefetch_frequecies=list(pmi.keys())
    #lst_prefetch_frequecies.append(w)
    #cache_frequencies(lst_prefetch_frequecies)
    #normalize frequency
    for key in pmi:
        if get_frequency(key)==0:
            pmi[key]=0
        else:
            pmi[key]=math.log(pmi[key]*get_word_count()/(get_frequency(key)*get_frequency(w)),2)
            if pmi[key]<0:pmi[key]=0;
        #pmi[key]=(pmi[key]*get_frequency(key)*get_frequency(w)/get_word_count())

def load_bigrams_from_file(word):
    for line in  open(os.path.join(dir_cache,"bigrams", word)).readlines():
        tokens=line.split()
        cfd[word][tokens[0]]=int(tokens[1]);

def init_cfd():
    for root, dirnames, filenames in os.walk(os.path.join(dir_cache,"bigrams")):
        for filename in fnmatch.filter(filenames, '*'):
            load_bigrams_from_file(filename)

def cache_cfd(w):
    if w in cfd: return;
    if PREFETCH_INDIVIDUAL_WORDS:
        if not os.path.isfile(os.path.join(dir_cache,"bigrams",w)):
            check_dir( os.path.join(dir_cache,"bigrams"))
            my_call(["../preprocess/get_bigrams", path_corpus,  os.path.join(dir_cache,"bigrams"), w], cwd="../preprocess")
    if os.path.isfile(os.path.join(dir_cache,"bigrams",w)):
        load_bigrams_from_file(w)

################ vectors #############
def vec_module(a):
    result=0
    for k in a.values():
        result+=k
    result=math.sqrt(result)
    return result

def cmp_vectors_cosine(a,b):
    result=0;
    #epsilon=0.0001
    keys = a.keys() & b.keys()
    for key in keys:
        result += a[key]*b[key]
#    return (result)/(vec_module(a)*vec_module(b)+1)
    return (result)/(vec_module(a)*vec_module(b))

metric = cmp_vectors_cosine
    
def cmp_vectors_euc(a,b):
    result=0;
    keys = a.keys() | b.keys()
    for key in keys:
        result += (a[key]-b[key])**2
    return 1/(math.sqrt(result)+1)

def cmp_words(a,b):
    return metric(collocation_measure(a),collocation_measure(b))
 
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
    return l[scores.index(max(scores))+1], confidence

def show_common_context(a,b,N=12):
    ca= get_cfd(a)
    cb= get_cfd(b)
    keys_a=[i[0] for i in ca.most_common(10)]
    keys_b=[i[0] for i in cb.most_common(10)]
    keys= set(keys_a) | set(keys_b)
    joint={}
    for k in keys:
        joint[k]=ca[k]+cb[k]
    genexp = ((k, joint[k]) for k in sorted(joint, key=joint.get, reverse=True))
    #return genexp
#    ordered = OrderedDict(sorted(joint.items()))
    #for kk in itertools.islice(genexp,0,N):
    for kk in genexp:
        k=kk[0]
        print (str(k).ljust(12),"\t",ca[k],"\t",cb[k])
    #return joint

####################   frequencies  #####################
def get_frequencies_from_corpora(lst):
    print ("extracting forrequencies from corpora ",len(lst),"requested")
    temp_freq=nltk.FreqDist()
    for line in open(path_corpus):
        for token in line.split():
            tkn_clean=token.strip()
            if(tkn_clean in lst):
                temp_freq[tkn_clean]+=1
    return temp_freq

#def get_frequencies_from_corpora2(lst):
    #print ("extracting forrequencies from corpora 2 ",len(lst),"requested")
 #   dump_list_to_file("../preprocess/words_of_interest.txt",lst)
  #  my_call(["../preprocess/get_frequency", path_corpus, os.path.join(dir_cache,"frequencies")], cwd="../preprocess")
   # prefetch_frequencies(lst)

#def cache_frequencies(l):
#    clean(l)
#    prefetch_frequencies(l)
#    lst = [w for w in l if not w in frequencies]
#    if len(lst)==0: 
#        return
#    check_dir(os.path.join(dir_cache,"frequencies"))
#    get_frequencies_from_corpora2(lst)

    #temp_freq=get_frequencies_from_corpora(lst)
    #print ("writing extracted frequencies to fs")
    #for k in temp_freq:
    #    dump_freq_to_file(k,temp_freq[k])
    #    frequencies[k]=temp_freq[k]

def dump_freq_to_file(w,freq):
    if not os.path.exists(os.path.join(dir_cache,"frequencies")):
        os.makedirs(os.path.join(dir_cache,"frequencies"))
    f = open(os.path.join(dir_cache,"frequencies",w),"w")
    f.write(str(freq))
    f.close()

#def prefetch_frequencies(l):
#    lst = [w for w in l if not w in frequencies]
    #print (len(frequencies),"frequencies in the list, ",len(l),"  requested to load")
#    for w in lst:
#        path_freq=os.path.join(dir_cache,"frequencies",w)
        #print(path_freq)
#        if os.path.isfile(path_freq):
#            frequencies[w] = int(open(path_freq).readline())
            #if frequencies[w]==0:
            #    print ("ow, prefetched 0 frequency for",w)
    #print (len(frequencies),"are now frequencies in the list, ")

def prefetch_frequencies_all():
    if not os.path.isfile(os.path.join(dir_cache,"frequencies")):
        my_call(["../preprocess/get_frequency_all", path_corpus, dir_cache], cwd="../preprocess")
    for line in open(os.path.join(dir_cache,"frequencies")):
        tokens=line.split()
        frequencies[tokens[0]]=int(tokens[1])

def get_frequency(w):
    if w[0]=='-': return get_frequency(w[1:])
    if w in frequencies:
        return frequencies[w]
    else:
        print ("oh frequency not in the list '",w,"'")
    return 0
    #print ("frequency was not in the list!")
    path_freq=os.path.join(dir_cache,"frequencies",w)
    if os.path.isfile(path_freq):
        frequencies[w] = int(open(path_freq).readline())
        return frequencies[w]
    counter = 0
    for line in open(path_corpus):
        for token in line.split():
            if(token.strip()==w):
                counter+=1
    dump_freq_to_file(w,counter)
    frequencies[w] = counter
    return frequencies[w]

def get_word_count():
    global cnt_words
    if cnt_words>0: return cnt_words
    name_file_cache=os.path.join(dir_cache,"word_count")
    if os.path.isfile(name_file_cache):
        return int(open(name_file_cache).readline())
    for line in open(path_corpus):
        cnt_words+=len(line.split())
    f = open(name_file_cache,"w")
    f.write(str(cnt_words))
    f.close()
    return cnt_words

def init():
    prefetch_frequencies_all()