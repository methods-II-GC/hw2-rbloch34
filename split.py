#!/usr/bin/env python


'''Program reads conll2000.tag (or another file with tags). Input is read and randomized according to seed
given by user. Input is split into 80% training data set, 10% development set, and 10% test set,
and written to file paths specified by user.'''


import random
import argparse

from typing import Iterator, List

def read_tags(path: str) -> Iterator[List[List[str]]]:
    with open(path, 'r') as source:
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

def write_tags(data, tag) -> Iterator[List[List[str]]]:
    with open(tag, 'w') as fhand:
        for line in data:
            for sent in line:
                word = " ".join(sent)
                # write word to file
                fhand.write(f"{word}\n")

def main(args: argparse.Namespace) -> None:
    corpus = list(read_tags(args.input))
    random.seed(args.seed)
    #specify split
    train_len = int((len(corpus)*0.8))
    dev_len = int((len(corpus)*0.1))
    test_len = int((len(corpus)*0.1))
    #shuffle
    random.shuffle(corpus)
    #split with indexing
    train = corpus[0:train_len]
    dev = corpus[train_len: train_len+dev_len]
    test = corpus[train_len+dev_len:]
    write_tags(train, args.train)
    write_tags(development, args.dev)
    write_tags(test, args.test)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='build a Python command-line tool which takes four arguments: input, train, dev, and test')
    parser.add_argument('--seed', type=int, required=True, help='Seed for random shuffling')
    parser.add_argument('input', type=str, help='Read input data')
    parser.add_argument('train', type=str, help='Path for writing training set')
    parser.add_argument('dev', type=str, help='Path for writing dev set')
    parser.add_argument('test', type=str, help='Path for writing test set')

    main(parser.parse_args())

