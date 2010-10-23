#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import itertools
import random
import sys

def stepped(iterable, n):
    "stepped(s, 3) => (s0,s1,s2), (s1,s2,s3), (s2, s3,s4), ..."
    iters = itertools.tee(iterable, n)
    for num, i in enumerate(iters):
        for _ in xrange(num):
            next(i, None)
    return itertools.izip(*iters)

def string_pairs_and_following(iterable):
    """
        string_pairs_and_following(['a','b','c','d'])
        => ('ab', 'c')
        => ('bc', 'd')
    """

    for a, b, c in stepped(iterable, 3):
        yield ("".join((a,b)), c)

def make_chain(names):
    """
        Generates a dictionary of letters that map to a list of letters that
        follow. Returns 'chain', the dictionary of letters, and 'first_letters',
        some good starting letters for words.
    """
    chain = {}
    first_letters = []
    for name in names:
        name = name.lower().strip()
        first_letters.append(name[:1])
        # the first two letters are often pretty good to start with, so add them
        first_letters.append(name[:2])

        # Make a chain that has two letters followed by a third
        for first, following in string_pairs_and_following(name):
            chain.setdefault(first, []).append(following)
        # In case that one fails, make a chain that has one letter
        # followed by another.
        for first, following in stepped(name, 2):
            chain.setdefault(first, []).append(following)
            
    return chain, first_letters

def make_chain_from_files(fnames):
    """
        Given a list of files as input, creates a markov chain for the lines in
        the files.
    """
    return make_chain([line for fname in fnames
                            for line in open(fname).readlines()])

def associate(chain, starting, shortest=3, longest=9):
    """ Evaluates the markov chain, generating a new word. """
    target_length = random.randint(shortest, longest)
    # Start off
    word = random.choice(starting)
    # Make the word
    while len(word) < target_length:
        # Get the next letter from the chain
        word += (
            # Best
            random.choice(chain.get(word[-2:], [None])) or
            # Plan B
            random.choice(chain.get(word[-1],  [None])) or
            # If all else fails
            random.choice("abcdefghijklmnopqrstuvwxyz")
        )
    return word.capitalize()

def generate_names(fnames, min_length=3, max_length=9):
    """ Generates names through markov chain association """
    chain, starting = make_chain_from_files(fnames)
    while True:
        yield associate(chain, starting, shortest=min_length, longest=max_length)

for name in itertools.islice(generate_names(sys.argv[1:]), 25):
    print name
