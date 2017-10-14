import sys


def main(args=None):
    """vsmlib cli entry point."""
    if args is None:
        args = sys.argv[1:]

    print("vsmlib CLI is comming soon.")
    print("for the time being please call modules directly ")
    print("e.g. python3 -m vsmlib.benchmarks.analogy config.yaml")


if __name__ == "__main__":
    main()