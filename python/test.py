#import nltk
#from nltk.collocations import *
#from nltk.corpus import stopwords
#import fnmatch
#import os
import vsmlib


m = vsmlib.Model_explicit()
m.load("/mnt/work/nlp_scratch/BNC_w3/")
#m.load("/storage/scratch/BNC/")
m_svd_scipy = vsmlib.Model_svd_scipy(m,300)
m_svd_scipy.save_to_dir("/mnt/work/nlp_scratch/BNC_w3_svd300/")

#m2 = vsmlib.model.Model_numbered()
#m2.load_from_dir("/storage/scratch/BNC_svd300")
#draw_features_and_similarity(m2,True) 
#print (m_svd_scipy.provenance)