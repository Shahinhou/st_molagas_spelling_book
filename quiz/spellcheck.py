#!/usr/bin/env python3

import sys
import re
from . import make_hashmap

def formatword(word):
    word = list(word)
    word.pop(0)
    word.pop()
    word = ''.join(word)
    return word.strip()

def makeline():
    print('-----------------')

def perform_test(f1, f2, answers=None):
    
    if answers==None:
        no_input_flag = False
    else:
        no_input_flag = True
        with open(answers) as f:
            answers = [c.strip() for c in f.readlines()]
        print(answers)

    correct = 0
    incorrect = 0
    errors = []

    answer_dict = {}


    with open(f1) as f:
        lines = [c.strip() for c in f.readlines()]

    questions = len(lines)

    for i, s in enumerate(lines):
        p = r'\[[a-zA-Z]*\]'
        word = formatword(re.findall(p,s)[0])
        print(word)
        print(re.sub(p, '_', s))
        print('Spell the missing word: ')

        if no_input_flag==False:
            s = input()
        else:
            s = answers[i]
        print(f'You wrote: {s}')
        
        if s.upper() == word.upper():
            correct += 1
        else:
            incorrect += 1
            errors.append(tuple((s, word, i)))

        answer_dict[i] = f'actual: {s}, expected: {word}'

    #print(errors)

    # test complete, return errors.

    #print(f'{correct}/{questions}\n({incorrect} incorrect entries)')
    
    return errors, correct, incorrect, lines, answer_dict

def classify_errors(errors, eng_file, unique_crit_file, reg_file):
    eng_to_crit = make_hashmap.make_map(eng_file)

    crit_to_reg = make_hashmap.make_eng_to_regex(unique_crit_file, reg_file)
    
    error_dict = {}
    #print(eng_to_crit)
    #print(crit_to_reg)
    for actual,expected,n in errors:

        error_dict[n] = []

        applicable_criteria = eng_to_crit[expected.lower()]
        #print(applicable_criteria)

        for crit in applicable_criteria:

            p = crit_to_reg[crit]
            print(p)

            if p == None or p == 'None':
                error_dict[n].append(f'erronious regex term for: {crit}')
                continue
            #print(p)

            matches = re.findall(p, actual)
            #print(matches)
            if len(matches) == 0:
                error_dict[n].append(crit)
    
    return error_dict




def make_breakdown_page(blank_html, errors, correct, incorrect, lines, error_dict, answer_dict):
    
    questions = len(lines)
    makepage.boiler(blank_html)

    for i, lines in enumerate(errors):
        n = lines[2]
        with open(blank_html, 'a') as f:
            if i == 0:
                f.write(f'<h2>{correct}/{questions}</h2>\n<h2>({incorrect} incorrect entries)</h2>\n')

            f.write('<div class="res">\n')
            f.write(f'<h2>Error {i}: </h2>\n')
            f.write(f'<p>Student entered: {lines[0]}</p>\n<p>Desired spelling: {lines[1]}</p>\n<p>(Step {lines[2]})</p>\n')
            f.write(f'<p>{answer_dict[n]}, failed criteria: {error_dict[n]}</p>')


            x = set(lines[0])
            y = set(lines[1])
            
            f.write(f'<p>Student included the following CORRECT letters: {(x.intersection(y))}\n</p>')
            f.write(f'<p>Student entered the following INCORRECT letters: {(x.difference(y))}\n</p>')
            f.write('</div>\n')
            f.write('<br><br>\n')

    makepage.closer(blank_html)






def main():
    errors, correct, incorrect, lines, answer_dict = perform_test(sys.argv[1], sys.argv[2], 'answers.txt')
    # in between, fetch errors and regexes.
    #print(answer_dict)
    error_dict = classify_errors(errors, 'no_bracket_criteria.txt', 'unique_criteria_list.txt', 'regex_expressions.txt')
    #print(error_dict)

    for n in error_dict.keys():
        makeline()
        print(f'{answer_dict[n]}, failed criteria: {error_dict[n]}')
        makeline()
    make_breakdown_page(sys.argv[2], errors, correct, incorrect, lines, error_dict, answer_dict)


if __name__=='__main__':
    main()
