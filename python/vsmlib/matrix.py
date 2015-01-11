import numpy as np
import scipy
import os

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
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def hello():
    print ("Hello 2!")

def load_int_from_file(name):
    return int(open(os.path.join(dir_root,name)).read())
    
def load_matrix_dok():
    cnt_unique_words=load_int_from_file("cnt_unique_words")
    #print (cnt_unique_words)
    cooccurrence = sparse.dok_matrix((cnt_unique_words,cnt_unique_words),dtype=np.float32)
    file_in=open(os.path.join(dir_root,"bigrams_list"))
    for line in file_in:
        tokens=line.split()
        cooccurrence[int(tokens[0]),int(tokens[1])]=float(tokens[2])
    file_in.close()
    return cooccurrence

def get_sparsity(x):
    if scipy.sparse.issparse(x):
        sparsity=(x.nnz)/(x.shape[0]*x.shape[1])
    else:
        sparsity=np.count_nonzero(ut)/(x.shape[0]*x.shape[1])
    return sparsity

def print_stats(m):
    print ("Matrix loaded")
    print ("Matrix dimentions : {} ({} unique words in the corpus )".format(m.shape,countof_fmt(m.shape[0])))
    size_float=64
    print ("Would take {} if stored in dense format".format(sizeof_fmt(size_float*m.shape[0]*m.shape[0])))
    print ("Cnt nonzero elements = {} (should take about {} of memory space".format(m.nnz,sizeof_fmt(m.nnz*size_float)))
    print ("Sparsity = {0:.4f}%".format(100*get_sparsity(m)))



def load_matrix_csr(path,dic_words_ids,zero_negatives=False):
    data = np.loadtxt(open(os.path.join(path,"bigrams.data")),dtype=np.float32)
    if zero_negatives:
        data[data<0]=0
    col_ind = np.loadtxt(open(os.path.join(path,"bigrams.col_ind")),dtype=int)
    row_ptr = np.loadtxt(open(os.path.join(path,"bigrams.row_ptr")),dtype=int)
    cooccurrence=scipy.sparse.csr_matrix((data,col_ind,row_ptr),shape=(len(dic_words_ids),len(dic_words_ids)),dtype=np.float32)
    return cooccurrence