import logging
import unittest
import vsmlib
from vsmlib.benchmarks import analogy

logging.basicConfig(level=logging.DEBUG)


class Tests(unittest.TestCase):

    def test_3cosadd(self):
        path_model = "./test/data/embeddings/text/plain_no_file_header"
        model = vsmlib.model.load_from_dir(path_model)
        options = {}
        options["path_dataset"] = "./test/data/benchmarks/analogy/"
        options["path_results"] = "/tmp/vsmlib/analogy"
        options["name_method"] = "3CosAdd"
        analogy.run(model, options)

    def test_3cosavg(self):
        path_model = "./test/data/embeddings/text/plain_no_file_header"
        model = vsmlib.model.load_from_dir(path_model)
        options = {}
        options["path_dataset"] = "./test/data/benchmarks/analogy/"
        options["path_results"] = "/tmp/vsmlib/analogy"
        options["name_method"] = "3CosAvg"
        analogy.run(model, options)

    def test_LRcos(self):
        path_model = "./test/data/embeddings/text/plain_with_file_header"
        model = vsmlib.model.load_from_dir(path_model)
        options = {}
        options["path_dataset"] = "./test/data/benchmarks/analogy/"
        options["path_results"] = "/tmp/vsmlib/analogy"
        options["name_method"] = "LRCos"
        analogy.run(model, options)

    def test_PairDistance(self):
        path_model = "./test/data/embeddings/text/plain_with_file_header"
        model = vsmlib.model.load_from_dir(path_model)
        options = {}
        options["path_dataset"] = "./test/data/benchmarks/analogy/"
        options["path_results"] = "/tmp/vsmlib/analogy"
        options["name_method"] = "PairDistance"
        analogy.run(model, options)
