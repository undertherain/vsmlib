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
print ("converting sigma")
a = np.load(os.path.join(path,"sigma.npy"))
print ("\tloaded numpy array",a.shape)
f = h5py.File(os.path.join(path,'vectors.h5p'), "w")
dest = f.create_dataset("sigma", a.shape, dtype='float32')
dest[:] = a
f.flush()


print ("converting vectors")
a = np.load(os.path.join(path,"vectors.npy"))
print ("\tloaded numpy array",a.shape)
dest = f.create_dataset("vectors", a.shape, dtype='float32')
dest[:] = a
   
f.flush()
f.close()
end = timer()
print("done in {:.2f}s".format(end-start))