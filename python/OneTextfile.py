# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import nltk
import sys
from nltk.collocations import *
import math

# <codecell>

from nltk.corpus import stopwords
ignore_words=stopwords.words('english')
ignore_words.append("thou")
ignore_words.append("shall")

# <codecell>

#raw = open('/mnt/storage/Corpora/BNC/all.txt').read().lower()
#tokens = nltk.word_tokenize(raw)

# <codecell>

#raw = open('corpus/clarissa1.txt').read().lower()
#words = nltk.word_tokenize(raw)
words=nltk.corpus.brown.words()
tokens = [w.lower() for w in words if len(w)>2 and not w.lower() in ignore_words]

# <codecell>

bigrams = nltk.bigrams(tokens)
#[i for i in bigrams]
#cfd = nltk.ConditionalFreqDist(bigrams)
#cfd["fast"].most_common(10)

# <codecell>

def get_bigrams_by_word(text,w,window_size=2):
    finder = BigramCollocationFinder.from_words(text,window_size)
    #finder = BigramCollocationFinder.from_words(self.tokens, window_size)
    finder.apply_freq_filter(2)
    ignored_words = stopwords.words('english')
    finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
    myfilter = lambda *w1: w not in w1
    finder.apply_ngram_filter(myfilter)
    #collocations = finder.nbest(bigram_measures.likelihood_ratio, num)\n',
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    #scored = finder.score_ngrams(bigram_measures.pmi)
    #scored = finder.score_ngrams(bigram_measures.likelihood_ratio)
    return scored

# <codecell>

#bi_fast = get_bigrams_by_word(tokens,"fast",window_size=2)
#bi_quick = get_bigrams_by_word(tokens,"quick",window_size=2)
#bi_stupid = get_bigrams_by_word(tokens,"stupid",window_size=2)
#bi_dumb = get_bigrams_by_word(tokens,"dumb",window_size=2)

# <codecell>

#len(bi_stupid)
#bi_fast[:10]

# <codecell>

#len(cfd_quick.keys()),len(cfd_fast.keys())

# <codecell>

#cmp_words("remote","control")
show_common_context("remote","mean",15)

# <codecell>

#cmp_first_tail(["fast","quick","tree","cold","apple","door"])
#print(cfd["door"])
#for i in cfd["door"]:
#    print (i)
#cfd["door"].values()
#import inspect
#inspect.getmembers(cfd["door"])
#cmp_words("remote","automatic")
#cmp_words("quick","fast")
show_common_context("remote","distant",15)

# <codecell>

#cmp_first_tail(["remote","distant","savage","automatic","mean"])
#cmp_first_tail(["apple","orange","star","fast","human"])
cmp_first_tail(["skinny","slim","star","fast","human"])

# <codecell>

cmp_first_tail(["detest","argue","hate","reveal","discover"])

# <codecell>

cmp_first_tail(["gracious","clever","pleasant","present","pretty"])

# <codecell>

cmp_first_tail(["predict","foretell","prevent","discover","decide"])
show_common_context("predict","decide")

# <codecell>

cmp_first_tail(["pensive","oppressed","caged","happy","thoughtful"])

# <codecell>

show_common_context("pensive","thoughtful",20)

# <codecell>


# <codecell>


# <codecell>


# <codecell>


