#!/usr/bin/env python3

import sys

def alphasort(f1):

    with open(f1) as f:
        lines = f.readlines()

    for s in sorted(lines):
        print(s.strip())




def main():

    alphasort(sys.argv[1])

if __name__=='__main__':
    main()
