#import nltk
#from nltk.collocations import *
#from nltk.corpus import stopwords
#import fnmatch
import os
import sys
import glob
sys.path.append("..")
import vsmlib
from vsmlib import testhelper 

dir_root ="/mnt/work/nlp_scratch/target"
files = glob.glob(dir_root+"/*")
for f in files:
	name  =  os.path.basename(f)
	print(name)
	dir_source=f
	m = vsmlib.Model_numbered()
	m.load_from_dir(dir_source)
	result = testhelper.do_synonyms_test(m,testhelper.get_test_from_toefl("../../tests/toefl/toefl"))
	with open(name+"_toefl.html", 'w') as fo:
		print(result,file=fo)

