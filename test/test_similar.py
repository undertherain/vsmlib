import unittest
from vsmlib.model import ModelNumbered

path = "/mnt/storage/Data/Embeddings/explicit_BNC_m100_w2_svd_d200"


class Tests(unittest.TestCase):

    def test_similarity(self):
        model = ModelNumbered()
        model.load_with_alpha(path)
        l = model.get_most_similar_words("apple", 12)
        for w, s in l:
            print(w, s)
        self.assertIsInstance(model, object)
