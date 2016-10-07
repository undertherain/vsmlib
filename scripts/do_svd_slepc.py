from mpi4py import MPI
import petsc4py
import slepc4py
import sys
import os
from slepc4py import SLEPc
from petsc4py import PETSc
import numpy as np
from timeit import default_timer as timer
import h5py
import shutil

def Print(*s):
	if rank==0:
		print(*s)

slepc4py.init(sys.argv)
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

Print ("init slepc \t done")

cnt_dimensions = 100

argv = sys.argv
if len(argv) < 2:
	print ("direcrory name required")
	exit()
	
path = argv[1]

opts = PETSc.Options()
mat=PETSc.Mat()

f = h5py.File(os.path.join(path,'cooccurrence_csr.h5p'), "r")
dim = f['row_ptr'].shape[0]-1
shape=(dim,dim)
A = mat.create(comm=PETSc.COMM_WORLD)
A.setSizes(shape)
A.setFromOptions()
A.setUp()
rstart, rend = A.getOwnershipRange()
del A
print ("I'm rank {} of {} running on {}, my wonrership range is from {} to {}".format(rank,size,MPI.Get_processor_name(),rstart,rend))
indptr  = (f['row_ptr'][rstart:rend+1]).astype(np.int32)
indices = (f['col_ind'][indptr[0]:indptr[-1]]).astype(np.int32)
data = f['data'][indptr[0]:indptr[-1]]
f.close()
Print ("load data\t done")

#csr=(A.indptr[rstart:rend+1] - A.indptr[rstart], A.indices[A.indptr[rstart]:A.indptr[rend]], A.data[A.indptr[rstart]:A.indptr[rend]])
csr=(indptr-indptr[0], indices, data)

B=mat.createAIJ((shape), bsize=1, csr=csr, comm=PETSc.COMM_WORLD)
B.setUp()
B.assemble()
name = os.path.basename(os.path.normpath(path))


start=timer()
S = SLEPc.SVD()
S.create()
S.setDimensions(nsv=cnt_dimensions, ncv=PETSc.DEFAULT, mpd=PETSc.DEFAULT)
#S.setType(SLEPc.SVD.Type.CROSS)
S.setType(SLEPc.SVD.Type.TRLANCZOS)
S.setOperator(B)
S.solve()
provenance = "applied SVD by SLEPc\n"
provenance += "cnt dimensions = {}\n".format(cnt_dimensions)
#S.getWhichSingularTriplets()
end=timer()
if  comm.rank==0:
	Print("\nsolve took",end-start,"\n")
	its = S.getIterationNumber()
	Print("Number of iterations of the method: %d" % its)
	eps_type = S.getType()
	Print("Solution method: %s" % eps_type)
	provenance += "solution method: %s\n" % eps_type
	nev, ncv, mpd = S.getDimensions()
	Print("Number of requested eigenvalues: %d" % nev)
	tol, maxit = S.getTolerances()
	Print("Stopping condition: tol=%.4g, maxit=%d" % (tol, maxit))
	nconv = S.getConverged()
	Print("Number of converged eigenpairs %d" % nconv)
	provenance += "cnt processes: {}\n" .format(comm.size) 
	provenance += "execution time: {:.2f}s\n" .format(end-start) 


dir_dest=os.path.join(path,"../_slepc",name+"_svd_d{}".format(cnt_dimensions))
if comm.rank==0:
	print("Writing to filesystem")
	if not os.path.exists(dir_dest):
		os.makedirs(dir_dest)

vr, wr = B.getVecs()
left=np.zeros((cnt_dimensions,rend-rstart),dtype=np.float32)
sigmas = np.zeros((cnt_dimensions),dtype=np.float32)
for i in range(cnt_dimensions):
    S.getVectors(i,vr,wr)
    sigmas[i] = S.getSingularTriplet(i)
    left[i]=np.array(vr)

projected=left.T

#print("rank",comm.rank," ",projected.shape,"rstart",rstart)
#np.save(os.path.join(dir_dest,"vectors{}.npy".format(comm.rank)),projected)
#	np.save(os.path.join(dir_dest,"sigma.npy"),sigmas)

shape =  (vr.getSize(),cnt_dimensions)

comm.barrier()
f = h5py.File(os.path.join(dir_dest,'vectors.h5p'), "w",driver='mpio', comm=comm)
dset = f.create_dataset("vectors", shape, dtype='float32')
dset[rstart:rend] = projected
f.flush()
comm.barrier()

dset_s = f.create_dataset("sigma", sigmas.shape, dtype='float32')
if comm.rank==0:
	dset_s[:] = sigmas
	shutil.copyfile(os.path.join(path,"ids"), os.path.join(dir_dest,"ids"))
	shutil.copyfile(os.path.join(path,"freq_per_id"), os.path.join(dir_dest,"freq_per_id"))

f.flush()
comm.barrier()

f.close()
if comm.rank==0:
	with open (os.path.join(path,"provenance.txt"), "r") as myfile:
		provenance = myfile.read() +"\n" +provenance
	text_file = open(os.path.join(dir_dest,"provenance.txt"), "w")
	text_file.write(provenance)
	text_file.close()
