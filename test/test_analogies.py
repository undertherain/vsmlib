import vsmlib
import vsmlib.benchmarks
import vsmlib.benchmarks.analogy

import unittest


class Tests(unittest.TestCase):

    def test_analogies(self):
        model = vsmlib.model.ModelDense()
        path_model = "./test/data/embeddings/text/plain/emb.txt"
        model.load_from_text(path_model)
        vsmlib.benchmarks.analogy.options["dir_root_dataset"] = "./test/data/"
        vsmlib.benchmarks.analogy.options["path_results"] = "/tmp/vsmlib/analogy"
        vsmlib.benchmarks.analogy.m = model  # todo this is ugly and should be fixed
        vsmlib.benchmarks.analogy.make_normalized_copy()

        vsmlib.benchmarks.analogy.run_all("benchmarks")
