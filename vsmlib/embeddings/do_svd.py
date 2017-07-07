import os
import sys
import shutil
sys.path.append("..")
import vsmlib
import numpy as np
import scipy.sparse.linalg
	
cnt_dimensions = 500
argv = sys.argv
if len(argv) < 2:
	print ("directory name required")
	exit()
dir_source = argv[1]

def factorize(cnt_dimensions):
	ut, s_ev, vt = scipy.sparse.linalg.svds(m.matrix,k=cnt_dimensions,which='LM',return_singular_vectors="u") # LM SM LA SA BE
	dir_dest=(os.path.join(dir_source,"../_factorized/",m.name+"_svd_d{}".format(cnt_dimensions)))
	if not os.path.exists(dir_dest):
		os.makedirs(dir_dest)
	#name = m.name+"_svd_s{}_a{}".format(cnt_dimensions,power)
	np.save(os.path.join(dir_dest,"vectors.npy"),ut)
	np.save(os.path.join(dir_dest,"sigma.npy"),s_ev)
	with open (os.path.join(dir_source,"provenance.txt"), "r") as myfile:
		provenance = myfile.read()
	provenance += "\napplied scipy.linal.svd, {} singular vectors".format(cnt_dimensions)
	#, sigma in the power of {} ,power
	text_file = open(os.path.join(dir_dest,"provenance.txt"), "w")
	text_file.write(provenance)
	text_file.close()
	shutil.copyfile(os.path.join(dir_source,"ids"), os.path.join(dir_dest,"ids"))
	shutil.copyfile(os.path.join(dir_source,"freq_per_id"), os.path.join(dir_dest,"freq_per_id"))
#provenence
		#self.sigma = s_ev
       	#sigma_p=np.power(s_ev, power)
       	#self.matrix =  np.dot(ut,np.diag(sigma_p))    


def do_svd_and_save(m):
	lst_pow_sigma=[1]
	for c in lst_pow_sigma:
		m_svd = vsmlib.Model_svd_scipy(m,cnt_dimensions,c)
		dir_dest=(os.path.join(dir_source,"../_converted/",m_svd.name))
		print (dir_dest)
		m_svd.save_to_dir(dir_dest)

m = vsmlib.Model_explicit()
m.load_from_hdf5(dir_source)

#for i in [100,200,300,400,500,600,700,800,900]:
#for i in [1000,1100,1200]:
#    cnt_dimensions=i
#    do_svd_and_save(m)

#print ("doing positive PMI")
#m.clip_negatives()

#do_svd_and_save(m)
factorize(cnt_dimensions)
