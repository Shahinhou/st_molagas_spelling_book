from django.shortcuts import render
from django import forms
import re
from .models import *
from . import spellcheck
from . import make_hashmap
from . import makepage
import datetime

# Create your views here.

class answerForm(forms.Form):
    answer = forms.CharField(label="Your Answer")

class loginForm(forms.Form):
    child = forms.CharField(label="Your Name")
    teacher = forms.CharField(label="Your Class")

def make_txt(child, teacher, crit_counter, breakdown, correct, incorrect):

    student = Student(name=child)
    student.save()
    teacher = Classroom.objects.get(name=teacher)

    teacher.students.add(student)

    critcount_str = [f'Error:  \t  No. of instances:\n{"-"*50}\n']+[f'{k}:  \t  {v}' for k,v in crit_counter.items()]
    critcount_str = '\n'.join(critcount_str)

    breakdown_str = '\n'.join(breakdown.values())
    student.result_sheet = f'Pupil Name: {child}\n\nDate: {datetime.date.today()}\n\nScore: {correct}/{incorrect}\n\nAnalysis:\n\n{critcount_str}\n\nBreakdown:\n\n{breakdown_str}'
    student.save()
    teacher.save()

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



def index(request):
    
    questions, server_answers, total = prep_qna('static/text/sample.txt')
    
    correct = 0
    incorrect = 0
    answer_dict = {}
    error_dict = {}
    errors = []

    if request.method == 'POST':

        form = loginForm(request.POST)

        if form.is_valid():
            
            child = request.POST.get('child')
            teacher = request.POST.get('teacher')

            request.session['child'] = child
            request.session['teacher'] = teacher
            
        elif 'child' in request.session and 'teacher' in request.session:
            pass

        else:
            return render(request, 'quiz/index.html', {
                'form': answerForm(),
                'questions': questions,
                'login_form': loginForm()
                })

        
        # if the request to the server is in the form of a user RETURNING data
        print('\n','posting','\n')
        form = answerForm(request.POST)
         
        if form.is_valid():
            
            user_answers = request.POST.getlist('answer')
            
            errors, correct, incorrect, answer_dict = correctify(user_answers, server_answers)

            # we have gotten our correct/incorrect, completed answer_dict.
            # we need to compose criteria/error_dict now.

            error_dict, crit_counter = spellcheck.classify_errors(errors, 
                    'static/text/no_bracket_criteria.txt', 
                    'static/text/unique_criteria_list.txt', 
                    'static/text/regex_expressions.txt')
            
            breakdown = {}
            for k,v in error_dict.items():

                breakdown[k] = f"Child's Answer: {answer_dict[k][0]}, Expected: {answer_dict[k][1]},\n Missing Criteria: {', '.join(v)}"
            
            print(breakdown)

            child = request.session['child']
            teacher = request.session['teacher']

            txt = make_txt(child, teacher, crit_counter, breakdown, correct, incorrect)

            return render(request, 'quiz/results.html', {
                'correct' : correct,
                'incorrect' : incorrect,
                'breakdown':breakdown,
                })
        else:
            return render(request, 'quiz/index.html', {
                'form': answerForm(),
                'login_form': loginForm(),
                'child': child,
                'teacher': teacher,
                'questions': questions
                })
    else:
        # this means they are just opening the site on index.

        return render(request, 'quiz/index.html', {
            'login_form': loginForm(),
            'form': answerForm(),
            'questions': questions
            })

