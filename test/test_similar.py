import unittest
import vsmlib

# path = "/mnt/storage/Data/Embeddings/explicit_BNC_m100_w2_svd_d200"
path = "test/data/embeddings/text/plain"


class Tests(unittest.TestCase):

    def test_similarity(self):
        model = vsmlib.model.load_from_dir(path)
        sims = model.get_most_similar_words("apple", 12)
        for w, s in sims:
            print(w, s)
        self.assertIsInstance(model, object)
