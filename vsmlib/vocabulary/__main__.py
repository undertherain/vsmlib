import os
import argparse
from vsmlib.vocabulary import create_from_dir


def main():
    parser = argparse.ArgumentParser(description='Create vocabulary from dir')
    parser.add_argument("src")
    parser.add_argument("dst")
    parser.add_argument('--min_frequency', type=int, default=1)

    args = parser.parse_args()

    if os.path.isdir(args.dst) and os.listdir(args.dst):
        print("destination dir is not empty")
        exit(-1)

    vocab = create_from_dir(args.src, args.min_frequency)
    vocab.save_to_dir(args.dst)


if __name__ == "__main__":
    main()
