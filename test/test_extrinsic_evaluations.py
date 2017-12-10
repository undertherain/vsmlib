import unittest
import vsmlib
import logging
import vsmlib.benchmarks.sequence_labeling.sequence_labeling
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
path = "test/data/embeddings/text/plain_with_file_header"


class Tests(unittest.TestCase):

    def test_sequence_labeling(self):
        path_model = "./test/data/embeddings/text/plain_with_file_header"
        model = vsmlib.model.load_from_dir(path_model)
        options = {}
        options['window'] = 2
        options['task'] = 'pos'
        options["path_dataset"] = "./test/data/benchmarks/sequence_labeling/pos/"
        vsmlib.benchmarks.sequence_labeling.sequence_labeling.run(model, options)