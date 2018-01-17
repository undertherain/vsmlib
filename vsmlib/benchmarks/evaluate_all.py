"""

this script evaluate all available benchmarks on vsmlib

"""
import argparse
import os
import sys
from vsmlib.benchmarks.analogy import analogy
from vsmlib.benchmarks.similarity import similarity
from vsmlib.benchmarks.sequence_labeling import sequence_labeling
import json

results_file_name = "results_0113.json"
test_morph = False
test_word_similarity = False
test_word_analogy_bats = True
test_word_analogy_google = False
test_sequence_labeling = False


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_root_dataset', default='/work/data/NLP/datasets/')
    parser.add_argument('--path_root_config', default='/home/bofang/vsmlib/vsmlib/benchmarks/')
    parser.add_argument('--path_json_output', default='/tmp/vsmlib/' + str(1) + '/')  # random.randint(0, 10000)
    parser.add_argument('--path_vector', help='path to the vector', required=True)

    args = parser.parse_args(args)
    return args


def get_file_name(json_data):
    print(json.dumps(json_data, sort_keys=True, indent=4))
    return json_data["task"] + "_" + json_data["dataset"] + "_" + json_data["method"] + "_" + json_data["measurement"]


def write_results(args, results):
    for result in results:
        print(result)
        file_name = get_file_name(result['experiment_setup'])
        print(file_name)
        with open(os.path.join(args.path_json_output, file_name + ".json"), 'w') as output:
            output.write(json.dumps(result, sort_keys=True, indent=4))


def run(args):
    args.path_vectors = args.path_vector
    if not os.path.isfile(os.path.join(args.path_vector, "vectors.h5p")) \
            and not os.path.isfile(os.path.join(args.path_vector, "vectors.txt")) \
            and not os.path.isfile(os.path.join(args.path_vector, "vectors.bin")):
        return

    if not os.path.exists(os.path.dirname(args.path_json_output)):
        os.makedirs(os.path.dirname(args.path_json_output))

    if test_word_similarity is True:
        args.path_dataset = os.path.join(args.path_root_dataset, 'similarity')
        args.path_config = os.path.join(args.path_root_config, 'similarity', 'config.yaml')
        tmp_results = similarity.main(args)
        write_results(args, tmp_results)

    if test_word_analogy_google is True:
        args.path_config = os.path.join(args.path_root_config, 'analogy', 'config_analogy.yaml')
        args.path_dataset = os.path.join(args.path_root_dataset, 'analogies', 'Google_dir')
        tmp_results = analogy.main(args)
        print(tmp_results)
        write_results(args, tmp_results)

    if test_word_analogy_bats is True:
        args.path_config = os.path.join(args.path_root_config, 'analogy', 'config_analogy.yaml')
        args.path_dataset = os.path.join(args.path_root_dataset, 'analogies', 'BATS_3.0')
        tmp_results = analogy.main(args)
        print(tmp_results)
        write_results(args, tmp_results)

    if test_sequence_labeling is True:
        tmp_results = []
        args.path_config = os.path.join(args.path_root_config, 'sequence_labeling', 'config.yaml')
        args.path_dataset = os.path.join(args.path_root_dataset, 'sequence_labeling', 'pos')
        args.task = 'pos'
        tmp_results.extend(sequence_labeling.main(args))

        args.path_dataset = os.path.join(args.path_root_dataset, 'sequence_labeling', 'chunk')
        args.task = 'chunk'
        tmp_results.extend(sequence_labeling.main(args))

        args.path_dataset = os.path.join(args.path_root_dataset, 'sequence_labeling', 'ner')
        args.task = 'ner'
        tmp_results.extend(sequence_labeling.main(args))

        write_results(args, tmp_results)


def main(args=None):
    args = parse_args(args)
    path_vector = args.path_vector

    run(args)
    for root, dirs, files in os.walk(path_vector, topdown=False):
        for name in dirs:
            args.path_vector = os.path.join(root, name)
            run(args)


if __name__ == "__main__":
    main()
