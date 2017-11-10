import logging
import unittest
import vsmlib
import vsmlib.benchmarks
import vsmlib.benchmarks.analogy
import vsmlib.benchmarks.analogy.analogy

logging.basicConfig(level=logging.DEBUG)


class Tests(unittest.TestCase):

    def test_3cosadd(self):
        path_model = "./test/data/embeddings/text/plain_no_file_header"
        model = vsmlib.model.load_from_dir(path_model)
        vsmlib.benchmarks.analogy.analogy.options["dir_root_dataset"] = "./test/data/benchmarks/analogy/"
        vsmlib.benchmarks.analogy.analogy.options["path_results"] = "/tmp/vsmlib/analogy"
        vsmlib.benchmarks.analogy.analogy.m = model  # todo this is ugly and should be fixed
        vsmlib.benchmarks.analogy.analogy.run_all("benchmarks")

    def test_3cosavg(self):
        path_model = "./test/data/embeddings/text/plain_no_file_header"
        model = vsmlib.model.load_from_dir(path_model)
        vsmlib.benchmarks.analogy.analogy.options["dir_root_dataset"] = "./test/data/benchmarks/analogy/"
        vsmlib.benchmarks.analogy.analogy.options["path_results"] = "/tmp/vsmlib/analogy"
        vsmlib.benchmarks.analogy.analogy.options["name_method"] = "3CosAvg"
        vsmlib.benchmarks.analogy.analogy.m = model
        vsmlib.benchmarks.analogy.analogy.run_all("benchmarks")

    def test_LRcos(self):
        path_model = "./test/data/embeddings/text/plain_with_file_header"
        model = vsmlib.model.load_from_dir(path_model)
        vsmlib.benchmarks.analogy.analogy.options["dir_root_dataset"] = "./test/data/benchmarks/analogy/"
        vsmlib.benchmarks.analogy.analogy.options["path_results"] = "/tmp/vsmlib/analogy"
        vsmlib.benchmarks.analogy.analogy.options["name_method"] = "LRCos"
        vsmlib.benchmarks.analogy.analogy.m = model
        vsmlib.benchmarks.analogy.analogy.run_all("benchmarks")

    def test_PairDistance(self):
        path_model = "./test/data/embeddings/text/plain_with_file_header"
        model = vsmlib.model.load_from_dir(path_model)
        vsmlib.benchmarks.analogy.analogy.options["dir_root_dataset"] = "./test/data/benchmarks/analogy/"
        vsmlib.benchmarks.analogy.analogy.options["path_results"] = "/tmp/vsmlib/analogy"
        vsmlib.benchmarks.analogy.analogy.options["name_method"] = "PairDistance"
        vsmlib.benchmarks.analogy.analogy.m = model
        vsmlib.benchmarks.analogy.analogy.run_all("benchmarks")
