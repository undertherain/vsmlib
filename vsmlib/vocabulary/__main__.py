import argparse
from vsmlib.vocabulary import create_from_dir


def main():
    parser = argparse.ArgumentParser(description='Create vocabulary from dir')
    parser.add_argument("src")
    parser.add_argument("dst")

    args = parser.parse_args()

    vocab = create_from_dir(args.src)
    print("the:", vocab.get_id("the"))

    # save to destination

if __name__ == "__main__":
    main()
