import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
import fnmatch
import os

matches = []
dir_root='/mnt/storage/Corpora/BNC/'
for root, dirnames, filenames in os.walk(dir_root):
  for filename in fnmatch.filter(filenames, '*.xml'):
      matches.append(os.path.join(root, filename)[len(dir_root):])
#matches
bnc=nltk.corpus.reader.bnc.BNCCorpusReader(dir_root,matches)
print (len(bnc.words()))
