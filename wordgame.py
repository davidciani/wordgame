#!/usr/bin/env python

import argparse, sys
from textwrap import fill
from itertools import permutations
from bisect import bisect_left
from pprint import pprint
from operator import itemgetter

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

def loadWordlist(wordlistfile=open(defaultWordlist)):
    wordlist = []
    for line in wordlistfile:
        wordlist.append(line.strip())
    return sorted(wordlist)

def findWords(hand,prefix='',suffix='',required='', wordlist=loadWordlist()):
    candidates = []
    hand = list(hand)
    hand.append(required)
    for i in range(1, len(hand)+1):
        for word in permutations(hand,i):
            word = prefix+''.join(word)+suffix
            if not str(word).find(required) and word not in candidates and search(wordlist,word):
                candidates.append(word)
                yield {
                    'word': word,
                    'score': score(word),
                    'length': len(word)
                }

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
    
    wordlist = loadWordlist(args.wordlistfile)
    
    results = findWords(args.hand,args.prefix,args.suffix,args.required,wordlist)

    print '{:<10}{:>8}{:>8}'.format('Word','Score','Length')
    print '-'*10+'-'*8+'-'*8

    for word in sorted(results,key=itemgetter('score','length'), reverse=True):
            print '{word:<10}{score:>8}{length:>8}'.format(**word)

if __name__ == "__main__":
    main()
