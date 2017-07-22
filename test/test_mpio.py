from mpi4py import MPI
import h5py

# 4 mpi ranks are assumed

rank = MPI.COMM_WORLD.rank

f = h5py.File('parallel_test.h5p', 'w', driver='mpio', comm=MPI.COMM_WORLD)

dset = f.create_dataset('test', (4,), dtype='i')
dset[rank] = rank

f.close()
