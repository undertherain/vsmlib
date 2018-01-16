"""

this script evaluate all available benchmarks on vsmlib

"""
import argparse
import os
from vsmlib.benchmarks.analogy import analogy
from vsmlib.benchmarks.similarity import similarity
from vsmlib.benchmarks.sequence_labeling import sequence_labeling
from vsmlib.benchmarks.morph_similarity import morph_similarity
import random

import json

results_file_name = "results_0113.json"
test_morph = False
test_word_similarity = False
test_word_analogy_bats = True
test_word_analogy_google = False
test_sequence_labeling = False

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_root_dataset', default = '/work/data/NLP/datasets/')
    parser.add_argument('--path_root_config', default = '/home/bofang/vsmlib/vsmlib/benchmarks/')
    parser.add_argument('--path_json_output', default = '/tmp/vsmlib/' + str(1) + '/') #random.randint(0, 10000)
    parser.add_argument('--path_vector', help='path to the vector', required=True)
    parser.add_argument('--print', default = 0, type=int)
    parser.add_argument('--write', default = 1, type=int)

    args = parser.parse_args()
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
    if 'context' in args.path_vector:
        return
    if 'e5' not in args.path_vector and 'e8' not in args.path_vector and 'e10' not in args.path_vector:
        return
    args.path_vectors = args.path_vector
    if not os.path.isfile(os.path.join(args.path_vector, "vectors.h5p")) \
            and not os.path.isfile(os.path.join(args.path_vector, "vectors.txt")) \
            and not os.path.isfile(os.path.join(args.path_vector, "vectors.bin")):
        return
    if os.path.isfile(os.path.join(args.path_vector, results_file_name)):
        t_r = os.stat(os.path.join(args.path_vector, results_file_name)).st_ctime
        t_e = os.stat(os.path.join(args.path_vector, "vectors.h5p")).st_ctime
        if t_r > t_e:
            if args.print == 1:
                print(args.path_vector, end="\t")
                json_data = open(os.path.join(args.path_vector, results_file_name)).read()
                if json_data.strip() == '':
                    print("empty json file")
                    return
                data = json.loads(json_data)
                if test_word_similarity is True:
                    print(data['similarity']['ws353'], end="\t")
                    print(data['similarity']['ws353_similarity'], end="\t")
                    print(data['similarity']['ws353_relatedness'], end="\t")
                    print(data['similarity']['luong_rare'], end="\t")
                    print(data['similarity']['sim999'], end="\t")
                    print(data['similarity']['bruni_men'], end="\t")
                    print(data['similarity']['luong_rare'], end="\t")
                    print("", end="\t")
                if test_word_analogy_google is True:
                    print(data['analogy_google']['g']['score'], end="\t")
                    print(data['analogy_google']['s']['score'], end="\t")
                    print("", end="\t")
                if test_word_analogy_bats is True:
                    print(data['analogy_bats']['I']['score'], end="\t")
                    print(data['analogy_bats']['D']['score'], end="\t")
                    print(data['analogy_bats']['E']['score'], end="\t")
                    print(data['analogy_bats']['L']['score'], end="\t")
                    print("", end="\t")
                if test_sequence_labeling is True:
                    print(data['sequence_labeling']['pos']['test'], end="\t")
                    print(data['sequence_labeling']['chunk']['test'], end="\t")
                    print(data['sequence_labeling']['ner']['test'], end="\t")
                    print("", end="\t")
                if test_morph is True:
                    print(data['morph']['morph']['none']['similarity'], end="\t")
                    print(data['morph']['morph']['HR']['similarity'], end="\t")
                    print(data['morph']['morph']['LR']['similarity'], end="\t")
                    print("", end="\t")
                print("")
            return




    if args.write == 1:
        with open(os.path.join(args.path_vector, results_file_name), 'w') as output:
            pass

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
        # rs = getAnalogyResults(tmp_results)
        # results['analogy_google'] = rs
        # print(json.dumps(results, sort_keys=True, indent=4))



    if test_word_analogy_bats is True:
        args.path_config = os.path.join(args.path_root_config, 'analogy', 'config_analogy.yaml')
        args.path_dataset = os.path.join(args.path_root_dataset, 'analogies', 'BATS_3.0')
        tmp_results = analogy.main(args)
        print(tmp_results)
        write_results(args, tmp_results)
        # rs = getAnalogyResults(tmp_results)
        # results['analogy_bats'] = rs
        # print(json.dumps(results, sort_keys=True, indent=4))




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


    if test_morph is True:
        args.path_dataset = os.path.join(args.path_root_dataset, 'morph_similarity',)
        args.path_config = os.path.join(args.path_root_config, 'morph_similarity', 'config.yaml')
        results['morph'] = morph_similarity.main(args)
        print(json.dumps(results, sort_keys=True, indent=4))






def main():
    args = parse_args()
    path_vector = args.path_vector

    run(args)
    for root, dirs, files in os.walk(path_vector, topdown=False):
        for name in dirs:
            args.path_vector = os.path.join(root, name)
            run(args)


if __name__ == "__main__":
    main()
