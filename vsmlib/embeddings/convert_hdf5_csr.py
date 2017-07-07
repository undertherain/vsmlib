import numpy as np
import h5py
import sys
import os
from timeit import default_timer as timer

argv = sys.argv
if len(argv) < 2:
    print ("direcrory name required")
    exit()
path = argv[1]

start = timer()
f = h5py.File(os.path.join(path, 'cooccurrence_csr.h5p'), "w")
print ("converting data")
a = np.fromfile(open(os.path.join(path, "bigrams.data.bin")), dtype=np.float32)
print ("\tloaded numpy array")
dset_data = f.create_dataset("data", a.shape, dtype='float32')
dset_data[:] = a
f.flush()

print ("converting col_ind")
a = np.fromfile(open(os.path.join(path, "bigrams.col_ind.bin")), dtype=np.int64)
print ("\tloaded numpy array")
dset_col_ind = f.create_dataset("col_ind", a.shape, dtype='int64')
dset_col_ind[:] = a
f.flush()

print ("converting row_ptr")
a = np.fromfile(open(os.path.join(path, "bigrams.row_ptr.bin")), dtype=np.int64)
print ("\tloaded numpy array")
dset_row_ptr = f.create_dataset("row_ptr", a.shape, dtype='int64')
dset_row_ptr[:] = a

f.flush()
f.close()
end = timer()
print("done in {:.2f}s".format(end - start))
