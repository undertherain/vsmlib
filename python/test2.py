import nltk
import similarity
import os
import fnmatch
import socket
import marisa

if socket.gethostname()=="cypress": similarity.path_corpus = "/storage/corpora/BNC/all.txt"
if socket.gethostname()=="ashtree":
	similarity.path_corpus = "/mnt/storage/Corpora/BNC/all.txt"
	similarity.dir_cache = "/mnt/work/nlp_scratch"


#print (similarity.cmp_words("pensive","rapid"))
#similarity.metric=similarity.cmp_vectors_cosine
#
similarity.collocation_measure=similarity.CollocationMeasures.pmi
r=similarity.cmp_first_tail(["pensive","oppressed","caged","happy","thoughtful"],verbose=True)
#rint(similarity.get_cfd_pmi("fast"))
print (r)
#print (similarity.get_cfd("fast").most_common(12))
#print (similarity.CollocationMeasures.pmi("quick").most_common(12))
#similarity.purge()
#similarity.cache_frequencies(["good","kind","best","happy","insane","mad","fast","forward","thoughtful","pensive","caged","dark","blue","green","greed","fear"])

