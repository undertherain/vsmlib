# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
import numpy
import matplotlib
import inspect

# <codecell>

from nltk.corpus import brown
len(brown.words())

# <codecell>

#mytext=nltk.Text(brown.words())
text = "I do not like green eggs and ham, I do not like them Sam I am!"
tokens = nltk.wordpunct_tokenize(text)
list(nltk.bigrams(tokens))
#finder = BigramCollocationFinder.from_words(tokens,3)
#finder = BigramCollocationFinder.from_documents(brown)
#scored = finder.score_ngrams(bigram_measures.raw_freq)
#sorted(bigram for bigram, score in scored)[:20]

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
    return scored[:20]
    

#sorted(scored)[:10]
#sorted((bigram for bigram, score in scored),10) 
#finder.nbest(bigram_measures.pmi, 10)  # doctest: +NORMALIZE_WHITESPACE

# <codecell>

words = nltk.corpus.brown.words()
ignored_words = stopwords.words('english')
text= [w.lower() for w in words if len(w) > 3 and not w.lower() in ignored_words]
bigrams = nltk.bigrams(text)
cfd = nltk.ConditionalFreqDist(bigrams)
print(cfd["fast"])
print(cfd["quick"])

# <codecell>

get_bigrams_by_word(text,"fast",window_size=3)

# <codecell>

get_bigrams_by_word(text,"quick",window_size=3)

# <codecell>

#load BNC
import fnmatch
import os

matches = []
dir_root='/mnt/storage/Corpora/BNC/B/'
for root, dirnames, filenames in os.walk(dir_root):
  for filename in fnmatch.filter(filenames, '*.xml'):
      matches.append(os.path.join(root, filename)[len(dir_root):])
#matches
bnc=nltk.corpus.reader.bnc.BNCCorpusReader(dir_root,matches)
len(bnc.words())

# <codecell>

#text2.collocations()
mytext=nltk.Text(bnc.words())

# <codecell>

get_bigrams_by_word(mytext,"skinny",window_size=4)

# <codecell>

get_bigrams_by_word(mytext,"thin",window_size=4)

# <codecell>

get_bigrams_by_word(mytext,"rapid",window_size=4)

# <codecell>

len(set(bnc.words()))

