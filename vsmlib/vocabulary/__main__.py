import argparse
from vsmlib.vocabulary import create_from_dir


def main():
    parser = argparse.ArgumentParser(description='Create vocabulary from dir')
    parser.add_argument("src")
    parser.add_argument("dst")

    args = parser.parse_args()

    vocab = create_from_dir(args.src)
    # todo check if dir is not empty
    vocab.save_to_dir(args.dst)


if __name__ == "__main__":
    main()
