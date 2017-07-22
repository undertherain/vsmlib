import vsmlib

m = vsmlib.model.ModelNumbered()
m.load_with_alpha("/home/blackbird/data/scratch/sparse/English/_slepc_/austen_m10_w2_svd_d200/", 0.1)

for i in m.get_most_similar_words("go"):
    print(i)
