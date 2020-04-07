import sys

USAGE = "<listen port> <output port>"


def main():
    if len(sys.argv) != 3:
        print("Invalid number of arguments.", USAGE)
        exit(-1)


if __name__ == "__main__":
    main()
