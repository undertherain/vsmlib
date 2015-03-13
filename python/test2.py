import os
import socket
import vsmlib
from matplotlib import pyplot as plt
#import marisa

#if socket.gethostname()=="cypress": similarity.path_corpus = "/storage/corpora/BNC/all.txt"
#if socket.gethostname()=="ashtree":
#	similarity.path_corpus = "/mnt/storage/Corpora/BNC/all.txt"
#	similarity.dir_cache = "/mnt/work/nlp_scratch"


#print (similarity.cmp_words("pensive","rapid"))
#similarity.metric=similarity.cmp_vectors_cosine
#
#similarity.collocation_measure=similarity.CollocationMeasures.pmi
#r=similarity.cmp_first_tail(["pensive","oppressed","caged","happy","thoughtful"],verbose=True)
#rint(similarity.get_cfd_pmi("fast"))
#print (r)
#print (similarity.get_cfd("fast").most_common(12))
#print (similarity.CollocationMeasures.pmi("quick").most_common(12))
#similarity.purge()
#similarity.cache_frequencies(["good","kind","best","happy","insane","mad","fast","forward","thoughtful","pensive","caged","dark","blue","green","greed","fear"])

#similarity.prefetch_frequencies_all()
#print (similarity.frequencies["fast"])

m=vsmlib.model.load_from_dir("/mnt/work/nlp_scratch/total_w3_POS_svd400_C0.1")
wordlist = ["horse","dog","cat","rabbi","cow","lion","elephant","donkey","goat","kangaroo","sheep","wolf"]
m.viz_wordlist(wordlist)
plt.show()