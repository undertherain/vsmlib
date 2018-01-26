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
import vsmlib.config
from multiprocessing import Pool
from multiprocessing import Process
import copy

c = vsmlib.config.load_config()
print(c)
print(c.Evaluate.path_root_dataset)

test_morph = c.Evaluate.test_morph
test_word_similarity = c.Evaluate.test_word_similarity
test_word_analogy_bats = c.Evaluate.test_word_analogy_bats
test_word_analogy_google = c.Evaluate.test_word_analogy_google
test_sequence_labeling = c.Evaluate.test_sequence_labeling


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_root_dataset', default=c.Evaluate.path_root_dataset)
    parser.add_argument('--path_root_config', default=c.Evaluate.path_root_config)
    parser.add_argument('--processes', type=int, help='processes to run the evaluation', default=10)
    parser.add_argument('--path_vector', help='path to the vector', required=True)
    parser.add_argument('--path_output', help='path to the output', required=True)
    parser.add_argument('--duplicate_folder', default=True)

    args = parser.parse_args(args)
    return args


def get_file_name(json_data):
    # print(json.dumps(json_data, sort_keys=True, indent=4))
    name = ''
    for key in c.Evaluate.folder_name_keys:
        if key in json_data:
            name += '_' + str(json_data[key])
    name = name[1:]
    return name


def get_default_embedding_folder(json_data):
    # print(json.dumps(json_data, sort_keys=True, indent=4))
    name = ''
    for key in c.Embedding.folder_name_keys:
        # print(key)
        if '.' in key:
            # print(key)
            if key.split('.')[1] in json_data[key.split('.')[0]]:
                name += '_' + str(json_data[key.split('.')[0]][key.split('.')[1]])
        else:
            if key in json_data:
                name += '_' + str(json_data[key])
    name = name[1:]
    return name


def write_results(args, results):
    for result in results:
        if 'result' in result:
            print(result['result'], end=', ')
    print('')
    for result in results:

        v = 0
        while True:
            embedding_folder_name = get_default_embedding_folder(result['experiment_setup']['embeddings'])
            embedding_folder_name += str(v)
            v += 1
            path = os.path.join(args.path_output, embedding_folder_name)
            if not os.path.exists(path):
                os.makedirs(path)
                break
            if args.duplicate_folder:
                break

        file_name = get_file_name(result['experiment_setup'])
        path = os.path.join(path, file_name + ".json")

        with open(path, 'w') as output:
            output.write(json.dumps(result, sort_keys=True, indent=4))


def run(args):
    args.path_vectors = args.path_vector
    if not os.path.isfile(os.path.join(args.path_vector, "vectors.h5p")) \
            and not os.path.isfile(os.path.join(args.path_vector, "vectors.txt")) \
            and not os.path.isfile(os.path.join(args.path_vector, "vectors.bin")):
        return

    print(args.path_vector)
    if test_word_similarity is True:
        args.path_config = os.path.join(args.path_root_config, c.Evaluate.word_similarity.config_folder_name,
                                        'config.yaml')
        args.path_dataset = os.path.join(args.path_root_dataset, c.Evaluate.word_similarity.dataset_folder_name)
        tmp_results = similarity.main(args)
        write_results(args, tmp_results)

    if test_word_analogy_google is True:
        args.path_config = os.path.join(args.path_root_config, c.Evaluate.word_analogy_google.config_folder_name,
                                        'config_analogy.yaml')
        args.path_dataset = os.path.join(args.path_root_dataset, c.Evaluate.word_analogy_google.dataset_folder_name)
        tmp_results = analogy.main(args)
        print(tmp_results)
        write_results(args, tmp_results)

    if test_word_analogy_bats is True:
        args.path_config = os.path.join(args.path_root_config, c.Evaluate.word_analogy_bats.config_folder_name,
                                        'config_analogy.yaml')
        args.path_dataset = os.path.join(args.path_root_dataset, c.Evaluate.word_analogy_bats.dataset_folder_name)
        tmp_results = analogy.main(args)
        print(tmp_results)
        write_results(args, tmp_results)

    if test_sequence_labeling is True:
        tmp_results = []
        for subtask in c.Evaluate.sequence_labeling.subtasks:
            args.path_config = os.path.join(args.path_root_config, c.Evaluate.sequence_labeling.config_folder_name,
                                            'config.yaml')
            args.path_dataset = os.path.join(args.path_root_dataset, c.Evaluate.sequence_labeling.dataset_folder_name,
                                             subtask)
            args.task = subtask
            tmp_results.extend(sequence_labeling.main(args))
        write_results(args, tmp_results)


def main(args=None):
    args = parse_args(args)
    path_vector = args.path_vector

    run(args)

    pool = Pool(processes=args.processes)

    argsList = []

    for root, dirs, files in os.walk(path_vector, topdown=False):
        for name in dirs:
            # print(name)
            args.path_vector = os.path.join(root, name)
            a = copy.deepcopy(args)
            argsList.append(a)
            # run(args)

    pool.map(run, argsList)
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
