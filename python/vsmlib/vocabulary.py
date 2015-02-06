import os
import numpy as np
import time

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def countof_fmt(num, suffix=''):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1000.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1000.0
    return "%.1f%s%s" % (num, 'Y', suffix)


class Vocabulary(object):
    def __init__(self):
        self.dic_words_ids={}
        self.lst_words=[]
    def get_id(self,w):
        try:
            return self.dic_words_ids[w]
        except KeyError:
            return -1
    def get_word_by_id(self,i):
        return(self.lst_words[i])

class Vocabulary_simple(Vocabulary):
    def load_dic_from_file(self,filename):
        rdic={}
        f=open(os.path.join(self.dir_root,filename), encoding='utf-8', errors='replace')
        lines=f.readlines()
        for line in lines:
            tokens=line.split()
            rdic[tokens[0]]=np.int64(tokens[-1])
        f.close()
        return rdic
    def load_list_from_file(self,filename,n):
        rlst=[""]*n
        #rlst=[]
        f=open(os.path.join(self.dir_root,filename), encoding='utf-8', errors='replace')
        lines=f.readlines()
        for line in lines:
            tokens=line.split()
            rlst[int(tokens[1])]=tokens[0]
         #   rlst.append(tokens[0])
        f.close()
        return rlst
    def load(self,path,verbose=False):
        self.dir_root=path
        self.dic_words_ids = self.load_dic_from_file("ids")
        self.lst_words=self.load_list_from_file("ids",len(self.dic_words_ids))

class Vocabulary_cooccurrence(Vocabulary_simple):
    def get_frequency(i):
        if i<0: return 0
        return(l_frequencies[i])
    def load(self,path,verbose=False):
        t_start=time.time()
        Vocabulary_simple.load(self,path)
        l_frequencies = np.fromfile(open(os.path.join(self.dir_root,"freq_per_id")),dtype=np.uint64)
        t_end=time.time()
        #assert len(self.lst_words)==len(self.dic_words_ids)
        if verbose:
            cnt_words=len(lst_words)
            print ("Vocabulary loaded in {0:0.2f} seconds".format(t_end-t_start))
            print ("{} words ({}) in vocabulary".format(cnt_words,countof_fmt(cnt_words)))

#dic_words_ids=None
#lst_words=[]
#dir_root=""

#def get_id(w):
    #try:
        #return dic_words_ids[w]
    #except :
        #return -1
    
#def get_word_by_id(i):
    #return(lst_words[i])

#def get_frequency(i):
    #if i<0: return 0
    #return(l_frequencies[i])

#def load_dic_from_file(filename):
    #rdic={}
    #f=open(os.path.join(dir_root,filename), encoding='utf-8', errors='replace')
    #lines=f.readlines()
    #for line in lines:
        #tokens=line.split()
        #rdic[tokens[0]]=np.int64(tokens[-1])
    #f.close()
    #return rdic

#def load(path,verbose=False):
	#t_start=time.time()
	#global dir_root,dic_words_ids,l_frequencies,lst_words
	#dir_root=path
	#dic_words_ids = load_dic_from_file("ids")
	#l_frequencies = np.fromfile(open(os.path.join(dir_root,"freq_per_id")),dtype=np.uint64)
	#lst_words=[]
	#lst_words=lst_words+([i[0] for i in sorted(dic_words_ids.items(), key=lambda x: x[1])])
	#t_end=time.time()
	#assert len(lst_words)==len(dic_words_ids)
	#if verbose:
		#cnt_words=len(lst_words)
		#print ("Vocabulary loaded in {0:0.2f} seconds".format(t_end-t_start))
		#print ("{} words ({}) in vocabulary".format(cnt_words,countof_fmt(cnt_words)))

#def report_rare():
	#for f in range(6):
		#cnt=0
		#for i in l_frequencies:
			#if i==f: cnt+=1
		#print ("words of frequency {}: {} of total {} - {:0.2f}%".format(f,countof_fmt(cnt), countof_fmt(len(l_frequencies)),100*cnt/len(l_frequencies)))

	#most_frequent = np.argsort(l_frequencies)[-10:]
 