#!/usr/bin/env python
"""
convert corpus to annotated corpus
This script uses nltk for dependency parsing, which is based on stanford corenlp.
"""
import os
from nltk.parse.stanford import *
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('corenlp_path',
                    help='Directory to stanford corenlp') # /home/lbf/Documents/stanford-corenlp-full-2017-06-09/
parser.add_argument('--max_block_size', '-mbs', default=1000000, type=int,
                    help='indicate how much charactors a parser deals at one time, bigger max_block_size will consume more memeory, but should be faster.')
parser.add_argument('--corpus_path', default='./news.toy.txt',
                    help='Directory to corpus')
parser.add_argument('--annotated_corpus_path', default='./news.toy.annotated.txt',
                    help='Directory to annotated corpus')
parser.add_argument('--parser_model', '-o', choices=['edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz', 'edu/stanford/nlp/models/parser/nndep/english_UD.gz'],
                    default='edu/stanford/nlp/models/parser/nndep/english_UD.gz',
                    help='stanford parser model')

args = parser.parse_args()

class dependency_parser():
    def __init__(self, path_to_jar, path_to_models_jar, model_path):
        if 'nndep/' in model_path:
            self.parser = StanfordNeuralDependencyParser(  #StanfordNeuralDependencyParser
                path_to_jar=path_to_jar,
                path_to_models_jar=path_to_models_jar,
                model_path=model_path, java_options='-mx5g') # , corenlp_options='-model modelOutputFile.txt.gz'
        if 'lexparser/' in model_path:
            self.parser = StanfordDependencyParser(
                path_to_jar=path_to_jar,
                path_to_models_jar=path_to_models_jar,
                model_path=model_path, java_options='-mx10g')

    def preprocess_text(self, text):
        # hack for nltk
        text = text.replace('/', '-')

        # hack for output format
        text = text.replace('{', '-')
        text = text.replace('}', '-')
        text = text.replace('[', '-')
        text = text.replace(']', '-')

        return text

    def parse(self, text):
        text = self.preprocess_text(text)
        out = ''
        # print(text)
        try:
            parse_results = self.parser.raw_parse(text) #, properties={'annotators' : 'depparse'}
            for dependency_tree in parse_results:
                for index, node in dependency_tree.nodes.items():
                    if node['word'] is None: # skip root node
                        continue
                    dependency_str = ''
                    for dep, index in node['deps'].items():
                        dependency_str += ',{}/{}'.format(str(index[0] - 1), dep)
                    dependency_str = dependency_str[1:]
                    out += '{}/{}[{}] '.format(node['word'], node['tag'], dependency_str)
                out += "\n"
            return out
        except AssertionError as e:
            print('error when parse "{}"'.format(text))
        return ''

dependency_parser = dependency_parser(
    path_to_jar=os.path.join(args.corenlp_path, "stanford-corenlp-3.8.0.jar"),
    path_to_models_jar=os.path.join(args.corenlp_path, "stanford-corenlp-3.8.0-models.jar"),
    model_path=args.parser_model)
    # edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz
    # edu/stanford/nlp/models/parser/nndep/english_UD.gz


start_time = time.time()

# dependency_parser.parse('Information about the stages 50km to 80km), booking for food and accommodation (R450-38 per night) and downloadable maps are on the Freedom Challenge website  call 00 27 84 567 4152 ')

block_size = 0
text = ''
with open(args.corpus_path, "r") as corpus_file, open(args.annotated_corpus_path, "w") as annotated_corpus_file:
    for line in corpus_file:
        text += line + "\n"
        block_size += len(line)
        if block_size > args.max_block_size:
            out = dependency_parser.parse(text)
            annotated_corpus_file.write(out)
            block_size = 0
            text = ''
    out = dependency_parser.parse(text)
    annotated_corpus_file.write(out)

end_time = time.time()
print('spend {} minutes'.format((end_time - start_time) / 60))

