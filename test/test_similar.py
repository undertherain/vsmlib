import unittest
import vsmlib

path = "test/data/embeddings/text/plain"


class Tests(unittest.TestCase):

    def test_similarity(self):
        model = vsmlib.model.load_from_dir(path)
        sims = model.get_most_similar_words("apple", cnt=12)
        for w, s in sims:
            print(w, s)
        self.assertIsInstance(model, object)
