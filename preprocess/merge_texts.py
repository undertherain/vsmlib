#!/usr/bin/env python3
import sys
import glob
import os
import re
import fnmatch

argv = sys.argv
if len(argv) < 3:
	print ("usage: input_dir output_file")
	exit()
name_dir = argv[1]
name_file_out = argv[2]

def is_line_valid(l):
	if len(l)<1: return False;
	if l[0]=="<": return False;
	return True;

def clean(l):
	#return l.lower().rstrip('\'\"-,.:;!?') 
	return re.sub('([a-z]+)[?:!.,;]*',r'\1',l.lower())

#files = glob.glob(name_dir+"/*")
files=[]
for root, dirnames, filenames in os.walk(name_dir,followlinks=True):
	for filename in fnmatch.filter(filenames, '*'):
		files.append(os.path.join(root, filename))

f_out = open(name_file_out,"w");
for name_file in files:
	print ("processing ",name_file)
	with open(name_file,errors="replace") as f:
		for line in f:
			if is_line_valid(line):
				#line=clean(line)
				line = clean(line)
				#print (line)
				f_out.write(line)

f_out.close()