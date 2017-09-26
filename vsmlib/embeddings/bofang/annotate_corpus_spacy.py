"""
convert corpus to annotated corpus
This script uses spacy for dependency parsing.
This spacy implementation is about 35 times faster than NLTK one.
"""

import spacy
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', '-bs', default=100000, type=int,
                    help='spacy batch size')
parser.add_argument('--n_threads', '-nt', default=32, type=int,
                    help='number of threads')
parser.add_argument('--max_block_size', '-mbs', default=20000000, type=int,
                    help='indicate how much lines a parser deals at one time, bigger max_block_size will consume more memeory, but should be faster.')
parser.add_argument('--corpus_path', default='./news.toy.txt',
                    help='Directory to corpus')
parser.add_argument('--annotated_corpus_path', default='./news.toy.annotated.txt',
                    help='Directory to annotated corpus')
args = parser.parse_args()


start_time = time.time()

nlp = spacy.load('en')


def getOutput(sent): # format a spacy Doc object for ouput
    out = ''
    for word in sent:
        out += '{}/{}[{}/{}] '.format(word.text, word.pos_, (word.head.i - word.i), word.dep_)
    out += "\n"
    return out


def annotate_to_file(textList, annotated_corpus_file):
    for doc in nlp.pipe(textList, batch_size=args.batch_size, n_threads=args.n_threads):
        for sent in doc.sents:
            out = getOutput(sent)
            annotated_corpus_file.write(out)
            annotated_corpus_file.write("\n")


textList = []
with open(args.corpus_path, "r") as corpus_file, open(args.annotated_corpus_path, "w") as annotated_corpus_file:
    for line in corpus_file:
        textList.append(line)
        print(line)
        # break
        # text = ['Australian scientist discovers star with telescope.']
        if len(textList) > args.max_block_size:  # parse text
            annotate_to_file(textList, annotated_corpus_file)
            textList = []
    annotate_to_file(textList, annotated_corpus_file)

end_time = time.time()
print('spend {} minutes'.format((end_time - start_time) / 60))