import os
import sys
import glob
sys.path.append("..")
import vsmlib
	
cnt_dimensions = 1000

argv = sys.argv
if len(argv) < 2:
	print ("direcrory name required")
	exit()
dir_source = argv[1]

def do_svd_and_save(m):
	lst_pow_sigma=[0.6]
	for c in lst_pow_sigma:
		m_svd = vsmlib.Model_svd_scipy(m,cnt_dimensions,c)
		dir_dest=(os.path.join(dir_source,"../!converted/",m_svd.name))
		print (dir_dest)
		m_svd.save_to_dir(dir_dest)

m = vsmlib.Model_explicit()
m.load(dir_source)
do_svd_and_save(m)

print ("doing positive PMI")
m.clip_negatives()

do_svd_and_save(m)