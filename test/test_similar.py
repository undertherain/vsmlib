import unittest
import vsmlib
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
path = "test/data/embeddings/text/plain"


class Tests(unittest.TestCase):

    def test_similarity(self):
        model = vsmlib.model.load_from_dir(path)
        sims = model.get_most_similar_words("apple", cnt=12)
        for w, s in sims:
            print(w, s)
        self.assertIsInstance(model, object)
        sims = model.get_most_similar_words("apple", cnt=12)
        model.normalize()
        logger.info("after normalization:")
        sims = model.get_most_similar_words("apple", cnt=12)
        for w, s in sims:
            print(w, s)
        logger.info("after normalized copy:")
        model = vsmlib.model.load_from_dir(path)
        model.cache_normalized_copy()
        sims = model.get_most_similar_words("apple", cnt=12)
        for w, s in sims:
            print(w, s)
