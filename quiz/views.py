from django.shortcuts import render
from django import forms
import re
from .models import Student, Test, Result, Classroom
from . import spellcheck
from . import make_hashmap
from . import makepage

# Create your views here.

class answerForm(forms.Form):
    answer = forms.CharField(label="Your Answer")

class userForm(forms.Form):
    user = forms.CharField(label="Your Name")

def prep_qna(file):

    server_answers = []
    
    with open(file) as f:
        questions = [s.strip() for s in f.readlines()]

    # prepare correct answers and list of questions
    p = r'\[[\S]*\]'
    for i,s in enumerate(questions):
        actual = re.findall(p,s)[0]
        print('\n',actual,'\n')
        server_answers.append(actual[1:len(actual)-1].strip())
        questions[i] = f'Q{i+1}: {re.sub(p, "(?)", s)}'

    total = len(questions)
    return questions, server_answers, total


def correctify(user_answers, server_answers):
    errors = []
    answer_dict = {} 
    correct = 0
    incorrect = 0
    for i,actual in enumerate(user_answers):

        expected = server_answers[i]
        if actual.lower() == expected.lower():
            correct += 1
        else:
            incorrect += 1
            errors.append(tuple((actual, expected, i)))

        answer_dict[i] = tuple((actual, expected))

    return errors, correct, incorrect, answer_dict

def login(request):

    if request.method=='POST':
        form = userForm(request.POST)

        if form.is_valid():
            username = request.POST.get('user')

            return index(request,username)
        else:
            return render(request, 'quiz/login.html', {
                'user_form': userForm()
                })

    return render(request, 'quiz/login.html', {
        'user_form': userForm()
        })

def index(request, user=None):
    
    questions, server_answers, total = prep_qna('static/text/sample.txt')
    
    correct = 0
    incorrect = 0
    answer_dict = {}
    error_dict = {}
    errors = []

    if request.method == 'POST':
        # if the request to the server is in the form of a user RETURNING data

        form = answerForm(request.POST)
         
        if form.is_valid():
            user_answers = request.POST.getlist('answer')
            
            errors, correct, incorrect, answer_dict = correctify(user_answers, server_answers)

            # we have gotten our correct/incorrect, completed answer_dict.
            # we need to compose criteria/error_dict now.

            error_dict = spellcheck.classify_errors(errors, 
                    'static/text/no_bracket_criteria.txt', 
                    'static/text/unique_criteria_list.txt', 
                    'static/text/regex_expressions.txt')
            
            breakdown = {}
            for k,v in error_dict.items():

                breakdown[k] = f"Child's Answer: {answer_dict[k][0]}, Expected: {answer_dict[k][1]},\n Missing Criteria: {', '.join(v)}"
            
            print(breakdown)
            return render(request, 'quiz/results.html', {
                'correct' : correct,
                'incorrect' : incorrect,
                'breakdown':breakdown,
                })
        else:
            return render(request, 'quiz/index.html', {
                'form': answerForm(),
                'user': user,
                'questions': questions
                })
    else:
        # this means they are just opening the site on index.

        return render(request, 'quiz/index.html', {
            'user': user,
            'form': answerForm(),
            'questions': questions
            })

