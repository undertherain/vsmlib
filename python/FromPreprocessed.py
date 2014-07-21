# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import nltk
import similarity
import os
import socket

# <codecell>

if socket.gethostname()=="cypress": similarity.path_corpus = "/storage/corpora/BNC/all.txt"

# <codecell>

#similarity.cmp_words("quick","fast")
similarity.cmp_words("pensive","fast")

# <codecell>

similarity.cmp_words("quick","fast")
similarity.show_common_context("fast","quick")

# <codecell>

#similarity.cmp_first_tail(cfdist,["remote","distant","savage","automatic","mean"])
#cmp_first_tail(cfdist,["fast","distant","quick","automatic","mean"])
similarity.show_common_context("fast","mean")

# <codecell>

similarity.show_common_context("remote","distant",15)

# <codecell>

similarity.cmp_first_tail(["detest","argue","hate","reveal","discover"])

# <codecell>

similarity.cmp_first_tail(["pensive","oppressed","caged","happy","thoughtful"])

# <codecell>

def do_synonyms_test(name_file):
    cnt_all=0;
    cnt_correct=0;
    for line in open(name_file).readlines():
        tokens = [token.lower() for token in line.split()]
        #print (tokens[0])
        guess=similarity.cmp_first_tail(tokens[:-1])
        if guess==tokens[-1]: cnt_correct+=1
        cnt_all+=1
        print (tokens[0],guess,guess==tokens[-1])
    success_rate=cnt_correct/cnt_all
    return success_rate

# <codecell>

do_synonyms_test("../tests/syn_easy.txt")

# <codecell>

similarity.cmp_first_tail(["kind","nice","best"],verbose=True)

# <codecell>

similarity.show_common_context("kind","nice")

# <codecell>

similarity.show_common_context("kind","best")

# <codecell>

similarity.frequency("fast")

# <codecell>

cfd = nltk.ConditionalFreqDist()
cfd["apple"]["orange"]=2.3
cfd["apple"]["orange"]

# <codecell>


# <codecell>


