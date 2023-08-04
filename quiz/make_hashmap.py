#!/usr/bin/env python3

import sys

# key to key, key to val
# eg:

# d1[word] = criteria, d2[criteria] = regex expression matching criteria.
# return regex expressions in sequence.

def make_set_of_criteria(d):
    #print(d) 
    unique_criteria = set()
    for v in d.values():
        #print(v)
        for c in v:
            unique_criteria.add(c)

    print(unique_criteria)
    for c in unique_criteria:
        print(c)


def make_eng_to_regex(test):

    # f1 = file of unique english criteria, ready-made.
    # f2 = file of regex per line matching english criteria, must be manual?

    # make compatible with sql text file.

    eng_to_reg = {}

    eng = [c.strip() for c in test.unique_crits.split('\n')]
    
    reg = [c.strip() for c in test.regs.split('\n')]

    for i,c in enumerate(eng):
        if reg[i][0] == 'r':
            eng_to_reg[c] = reg[i][2:-1]
        else:
            eng_to_reg[c] = None

    for k,v in eng_to_reg.items():
        #print(f'{k}: {v}')
        pass

    return eng_to_reg


def make_map(test):

    criteria_map = {}

    text = [c.strip() for c in test.crit_list.split('\n')] 
    
    #print(text)
    for lines in text:

        #print(lines)

        lines = lines.split(',')
        word = lines[0].lower()
        lines.pop(0)

        criteria_map[word] = []
        
        for c in lines:
            criteria_map[word].append(c.strip())

        for k,v in criteria_map.items():
           #print(f'{k}: {v}')
           pass

        #print(criteria_map)
    return criteria_map

def main():

    #file = sys.argv[1]
    #d = make_map(file)

    #make_set_of_criteria(d)

    make_eng_to_regex('unique_criteria_list.txt', 'regex_expressions.txt')

if __name__=='__main__':
    main()
