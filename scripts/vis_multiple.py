#!/usr/bin/env python3

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
from vsmlib.visualize import draw_features,draw_features_and_similarity,plotvectors,wordlist_to_rows,rows_to_img_array,std_to_img
import vsmlib.visualize
import random
import numpy as np

#dir_root ="/storage/scratch/SVD"
#dir_root ="/mnt/work/nlp_scratch/SVD/"
dir_root ="/home/blackbird/data/scratch"
sources = []
#sources.append("explicit_BNC_w3_pos_svd_400_C0.1")
sources.append("SVD/explicit_BNC_w5_pos_svd_1000_C0.1")
#sources.append("SVD/explicit_BNC_w3_pos_svd_400_C0.1")
#sources.append("glove/glove_300")
sources.append("glove/glove.6b.wiki_giga")

def output_img(wordlist,name):
	rows=wordlist_to_rows(m,wordlist)
#	im = rows_to_img_array(rows)
	im = vsmlib.visualize.rows_to_img_tips(rows)
	name_image=name+"_"+m.name+".png"
	im.save(os.path.join("pics",name_image))
	file_out.write(name+":<br />")
	htext = "<img src=\"pics/"+name_image+"\"/><br />"
	file_out.write(htext)
	row_std = np.std(rows, axis=0, dtype=None, out=None, keepdims=False)
	#row_std.shape=(1,rows.shape[1])
	im = std_to_img(row_std)
	name_image="std_"+name+"_"+m.name+".png"
	im.save(os.path.join("pics",name_image))
	file_out.write("<br />std:<br />")
	htext = "<img src=\"pics/"+name_image+"\"/><br />"
	file_out.write(htext)
	avg_std=np.mean(row_std)
	file_out.write("mean std = {}<br /><br />".format(avg_std))



file_out = open('plots.html','w')
htext = """<html>
<head>
 <link rel="stylesheet" type="text/css" href="mystyle.css">
</head>
<body>"""
file_out.write(htext)

#write all animals and verbs:
for name_file_dataset in glob.glob("../../data/clusters_manual/*.txt"):
	f_in=open(name_file_dataset)
	wordlist = [s.strip() for s in f_in.readlines()]
	f_in.close()
	file_out.write("<strong>"+os.path.basename(name_file_dataset)+"</strong> ")
	file_out.write(" ["+str(len(wordlist))+"]")
	file_out.write("<br />")
	file_out.write(str(wordlist))
	file_out.write("<br /><br />")



for source in sources:
	dir_source = os.path.join(dir_root,source)
	print ("opening "+source+" ...")
	m = vsmlib.model.load_from_dir(dir_source)
	print ("normalizing ...")
	#m.normalize()
	print ("done\n")
	file_out.write("<hr /><pre>")
	file_out.write("model: " +m.name)
	file_out.write(m.provenance)
	file_out.write("</pre><br />")

	for name_file_dataset in glob.glob("../../data/clusters_manual/*.txt"):
		f_in=open(name_file_dataset)
		wordlist = [s.strip() for s in f_in.readlines()]
		f_in.close()
		print(name_file_dataset,len(wordlist))
		output_img(wordlist,os.path.basename(name_file_dataset))

#	wordlist = [s.strip() for s in open("../../data/animals.txt").readlines()]
	#output_img(wordlist,"animals "+str(len(wordlist)))

	cnt_random_words=100
	wordlist = [random.choice(m.vocabulary.lst_words) for i in range(cnt_random_words)]
	output_img(wordlist,"random 100" )

	print ("generating images done\n\n")


htext = """</body>
</html>
"""
file_out.write(htext)
file_out.close()

