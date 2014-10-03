#!/usr/bin/env python

import argparse, sys
from textwrap import fill
from itertools import permutations
from bisect import bisect_left

num = {
        1 : 'one',
        2 : 'two',
        3 : 'three',
        4 : 'four',
        5 : 'five',
        6 : 'six',
        7 : 'seven',
        8 : 'eight',
        }
values = {
    'a': 1,
    'b': 4,
    'c': 4,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 3,
    'h': 3,
    'i': 1,
    'j': 10,
    'k': 5,
    'l': 2,
    'm': 4,
    'n': 2,
    'o': 1,
    'p': 4,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 2,
    'v': 5,
    'w': 4,
    'x': 8,
    'y': 3,
    'z': 10,
}

defaultWordlist = "/usr/share/dict/enable1.txt"

# Removes Duplicates from a list
def removeDuplicates(lst):
    lst.sort()
    last = lst[-1]
    for i in range(len(lst)-2,-1,-1):
        if last == lst[i]:
            del lst[i]
        else:
            last = lst[i]

def search(lst,item):
    return (item <= lst[-1]) and (lst[bisect_left(lst, item)] == item)

def score(str):
    scoresum = 0
    for letter in str:
        scoresum = scoresum + values[letter]
    return scoresum

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', dest='wordlistfile',
            type=argparse.FileType('r'),
            default=defaultWordlist);
    parser.add_argument('-p','--prefix', dest='prefix', default='')
    parser.add_argument('-s','--suffix', dest='suffix', default='')
    parser.add_argument('-r','--required', dest='required', default='')
    parser.add_argument('-v','--verbose', action='store_true')
    parser.add_argument('hand')

    args = parser.parse_args()

    wordlist = []
    for line in args.wordlistfile:
        wordlist.append(line.strip())
    wordlist.sort()

    candidates = {}
    for i in range(1, len(args.hand)+1):
        candidates[i] = []
        hand = list(args.hand)
        hand.append(args.required)
        for permutation in permutations(hand,i):
            if(str(permutation).find(args.required) >= 0):
                candidates[i].append(args.prefix+''.join(permutation)+args.suffix)
    if args.verbose:
       print candidates

    words = {}

    for k,v in candidates.iteritems():
        words[k] = []
        removeDuplicates(v);

        for word in v:
            if search(wordlist,word):
                words[k].append(word);


    for k in sorted(words.keys(),reverse=True):
        if len(words[k]) == 0:
            continue

        print str(len(words[k])) + " " + num[k+len(args.prefix)+len(args.suffix)] + " letter words found: "

        output = ""
        for i in range(len(words[k])):
            output = output + "{}{} ".format(words[k][i],score(words[k][i]))
        print fill(output,60)

if __name__ == "__main__":
    main()
