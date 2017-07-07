#!/usr/bin/env python3
import os
import sys
import glob
sys.path.append("..")
import vsmlib
import numpy as np
from pandas.tools.plotting import parallel_coordinates
import matplotlib as mpl
from matplotlib import pyplot as plt
import brewer2mpl
import sklearn
import sklearn.decomposition
import pandas

mpl.rcParams['figure.figsize'] = (24.0, 8.0)

argv = sys.argv
if len(argv) < 2:
	print ("direcrory name required")
	exit()
dir_root = argv[1]

mymodel=vsmlib.model.load_from_dir(dir_root)
mymodel.normalize()

def wordlist_from_pairs(name):
    with open(name) as f:
        pairs = [y for y in [x.split() for x in f.readlines() if len(x)>3]]
        wordlist = [item for sublist in pairs for item in sublist]
    return wordlist

wordlist = wordlist_from_pairs("../../data/pairs/verbs.txt")
#print (wordlist)
mycolors=brewer2mpl.get_map("Dark2","Qualitative",3).mpl_colors
#brewer2mpl.print_maps_by_type("Qualitative")

ax = plt.subplot('111')
#set_ax_params(ax)

rows = np.empty((0,mymodel.matrix.shape[1]))
for i in wordlist:
#    rows =np.vstack([rows,mymodel.get_row(i).todense()])
    rows =np.vstack([rows,mymodel.get_row(i)])
pca = sklearn.decomposition.PCA(n_components=7,whiten=True)
p = pca.fit_transform(rows)
df = pandas.DataFrame(p, index=["transitive","intransitive"]*int(p.shape[0]/2))
df.reset_index(level=0, inplace=True)

parallel_coordinates(df,"index",alpha=0.6)

ax.text(0.08,1.7,mymodel.provenance)
#plt.grid(b=False, which='major', axis='x', color="#aaaaaa", linestyle='--', linewidth=0)
#plt.grid(b=False, which='major', axis='y', color="#999999", linestyle='--')
#plt.grid(b=False, which='minor', color='r', linestyle='--')
#legend = plt.legend(frameon = 1)
#frame = legend.get_frame()
#frame.set_facecolor("#111111")
#frame.set_edgecolor('#aaaaaa')
#for text in legend.get_texts():
    #text.set_color(text_color)
plt.savefig("parallel_"+mymodel.name+"_verbs.pdf", bbox_inches='tight',transparent=True)