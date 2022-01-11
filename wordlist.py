def read_wordlist(path):
    with open(path) as f:
        return [line.rstrip() for line in f.readlines()]
