#echo $1
mpirun -np 4 --hostfile ./hostfile  --map-by node python3 do_svd_slepc.py $1
#"/home/blackbird/data/scratch/sparse/English/austen_m10_w2/"

