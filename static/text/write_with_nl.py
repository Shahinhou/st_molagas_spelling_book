#!/usr/bin/env python3

import sys

def write_with_newline(f1):

    with open(f1) as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        sys.stdout.write(line)
        sys.stdout.write('\\n')


def main():

    write_with_newline(sys.argv[1])

if __name__=='__main__':
    main()
