import os
import argparse
from vsmlib.vocabulary import create_from_dir


def main():
    parser = argparse.ArgumentParser(description='Create vocabulary from dir')
    parser.add_argument("src")
    parser.add_argument("dst")

    args = parser.parse_args()

    if os.path.isdir(args.dst) and os.listdir(args.dst):
        print("destination dir is not empty")
        exit(-1)

    vocab = create_from_dir(args.src)
    vocab.save_to_dir(args.dst)


if __name__ == "__main__":
    main()
