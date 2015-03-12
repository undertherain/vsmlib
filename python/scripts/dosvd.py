#import nltk
#from nltk.collocations import *
#from nltk.corpus import stopwords
#import fnmatch
import os
import sys
import glob
sys.path.append("..")
import vsmlib
	

#dir_root="/mnt/work/nlp_scratch/"
dir_root="/storage/scratch/"
positive = True

source ="test"
dir_source = os.path.join(dir_root,source)
name = os.path.basename(os.path.normpath(dir_source))
cnt_vectors=4
m = vsmlib.Model_explicit()
m.load(dir_source)
for c in [0.1,0.3,0.6,1]:
	if positive: 
		newname=name + "_TMP"
	else:
		newname = name

#	newname = newname+"_svd{}_C{}".format(cnt_vectors,c)
	m_svd = vsmlib.Model_svd_scipy(m,cnt_vectors,c)
	dir_dest=(os.path.join(dir_source,"../totest/",m_svd.name))
	print (dir_dest)
	m_svd.save_to_dir(dir_dest)

#m2 = vsmlib.model.Model_numbered()
#m2.load_from_dir("/storage/scratch/BNC_svd300")
#draw_features_and_similarity(m2,True) 
#print (m_svd_scipy.provenance)