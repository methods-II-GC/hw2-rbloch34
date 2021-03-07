#!/usr/bin/env python


'''Program reads conll2000.tag (or another file with tags). Input is read and randomized according to seed
given by user. Input is split into 80% training data set, 10% development set, and 10% test set,
and written to file paths specified by user.'''


import random
import argparse

from typing import Iterator, List

def read_tags(path: str) -> Iterator[List[List[str]]]:
    with open(path, "r") as source:
        lines = []
        for line in source:
            line = line.rstrip()
            if line:  # Line is contentful.
                lines.append(line.split())
            else:  # Line is blank.
                yield lines.copy()
                lines.clear()
    # Just in case someone forgets to put a blank line at the end...
    if lines:
        yield lines

def write_tags(text, path, start, size):
    with open(path, 'r') as file:
        for line in text[start:start + size]:
            file.write(line)

def main(args: argparse.Namespace) -> None:
    corpus = list(read_tags(args.input))
    random.seed(args.seed)
    random.shuffle(corpus)
    train = (len(corpus)*0.8)
    development = (len(corpus)*0.1)
    test = (len(corpus)*0.1)
    write_tags(corpus, args.train, 0, train)
    write_tags(corpus, args.dev, train, development)
    write_tags(corpus, args.test, train+development, test)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='build a Python command-line tool which takes four arguments: input, train, dev, and test')
    parser.add_argument('--seed', type=int, help='Seed for random shuffling')
    parser.add_argument('input', type=str, help='Read input data')
    parser.add_argument('train', type=str, help='Path for writing training set')
    parser.add_argument('dev', type=str, help='Path for writing dev set')
    parser.add_argument('test', type=str, help='Path for writing test set')

    namespace = parser.parse_args()
    main(namespace)
