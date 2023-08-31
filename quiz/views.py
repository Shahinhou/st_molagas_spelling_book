from django.shortcuts import redirect, render
from django import forms
import re
from .models import *
from . import spellcheck
from . import make_hashmap
from . import makepage
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

class answerForm(forms.Form):
    answer = forms.CharField(label="Your Answer")

class loginForm(forms.Form):
    child = forms.CharField(label="Your Name")
    teacher = forms.CharField(label="Your Class")

class testForm(forms.Form):
    options = [(obj.id, obj) for i,obj in enumerate(Test.objects.all())]
    test = forms.ChoiceField(choices=options)

def make_txt(child, teacher, crit_counter, breakdown, correct, incorrect, step_dict, other_crit):
    breakdown_str = '\n'.join(breakdown.values())
    # k is criteria
    critcount_str = [f'Error: No. of instances:']+[f'{step_dict[k]},{k},{len(v)},{v}' for k,v in crit_counter.items()]
    other_str = [f'Global Criteria: No. of instances:']+[f'{k},{v}' for k,v in other_crit.items()]

    critcount_str = '\n'.join(critcount_str)+'|'+'\n'.join(other_str)
    print(f'critcount: {critcount_str}')
    
    student = Student(name=child, breakdown=breakdown_str, crit_counter=critcount_str,correct=correct,incorrect=incorrect)
    student.save()
    teacher = Classroom.objects.get(name=teacher)

    teacher.students.add(student)


    breakdown_str = '\n'.join(breakdown.values())
    student.result_sheet = f'Pupil Name: {child}\n\nDate: {datetime.date.today()}\n\nScore: {correct}/{incorrect}\n\nAnalysis:\n\n{critcount_str}\n\nBreakdown:\n\n{breakdown_str}'
    student.save()
    teacher.save()

def prep_qna(test):

    server_answers = []
    #step_dict = 'lol'

    with open(test.steps) as f:
        
        s = [s.strip().split(',') for s in f.readlines()]
        #print(s)
        step_dict = {k.strip() : v.strip() for k,v in s}
    
    with open(test.questions) as f:
        questions = [s.strip() for s in f.readlines()]
    
    #questions = [s.strip() for s in test.questions.split('\n')]

    # prepare correct answers and list of questions
    p = r'\[[\S]*\]'
    for i,s in enumerate(questions):
        actual = re.findall(p,s)[0]
        server_answers.append(actual[1:len(actual)-1].strip())
        questions[i] = f'Q{i+1}: {re.sub(p, "(?)", s)}'

    total = len(questions)
    return questions, server_answers, total, step_dict


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

def update_dict(x, d):

    if x not in d:
        d[x] = 0

    d[x] += 1
    return d

def other_crit_check(test, server_answers, user_answers):

    other_crit_breakdown = {}

    with open(test.other_crit) as f:
        criteria = [s.strip().split(',') for s in f.readlines()]

    for i, answers in enumerate(server_answers):

        for j, letters in enumerate(answers):

            for k, crit in enumerate(criteria):

                if j < len(user_answers[i]) and letters == crit[0] and user_answers[i][j] == crit[1]:
                    #other_crit_breakdown.append(crit[2])

                    other_crit_breakdown = update_dict(crit[2], other_crit_breakdown)

                elif j < len(user_answers[i]) and letters == crit[1] and user_answers[i][j] == crit[0]:
                    #other_crit_breakdown.append(crit[2].strip())
                    
                    other_crit_breakdown = update_dict(crit[2], other_crit_breakdown)

    return other_crit_breakdown

@login_required(login_url='/accounts/login/')
def index(request):


    if request.user.username == 'teacher':
        return redirect("grades:index") # redirect to your page
    
    # questions, server_answers, total = prep_qna(test)
    teacher_names = [c.name for c in Classroom.objects.all()]
    
    correct = 0
    incorrect = 0
    answer_dict = {}
    error_dict = {}
    errors = []

    if request.method == 'POST':

        form = loginForm(request.POST)
        test_form = testForm(request.POST)

        if form.is_valid() and test_form.is_valid():
            
            child = request.POST.get('child')
            teacher = request.POST.get('teacher')
            test = request.POST.get('test')
            
            if teacher not in teacher_names:
                return render(request, 'quiz/index.html', {
                    'form': answerForm(),
                    'test_form': testForm(),
                    'login_form': loginForm()
                    })


            request.session['child'] = child
            request.session['teacher'] = teacher
            request.session['test'] = Test.objects.get(pk=test).name
            
        elif 'child' in request.session and 'teacher' in request.session:
            pass

        else:
            return render(request, 'quiz/index.html', {
                'form': answerForm(),
                'login_form': loginForm(),
                'test_form': testForm()
                })

        
        # if the request to the server is in the form of a user RETURNING data
        form = answerForm(request.POST)
         
        if form.is_valid():
            
            test = Test.objects.get(name=request.session['test'])

            questions, server_answers, total, step_dict = prep_qna(test)
            
            user_answers = request.POST.getlist('answer')
            
            errors, correct, incorrect, answer_dict = correctify(user_answers, server_answers)

            # we have gotten our correct/incorrect, completed answer_dict.
            # we need to compose criteria/error_dict now.

            error_dict, crit_counter = spellcheck.classify_errors(errors, test) 
            
            breakdown = {}
            for k,v in error_dict.items():

                breakdown[k] = f"Child's Answer: {answer_dict[k][0]}, Expected: {answer_dict[k][1]},\n Missing Criteria: {', '.join(v)}"
            

            child = request.session['child']
            teacher = request.session['teacher']

            other_crit = other_crit_check(test,server_answers,user_answers)

            txt = make_txt(child, teacher, crit_counter, breakdown, correct, incorrect, step_dict, other_crit)


            return render(request, 'quiz/results.html', {
                'correct' : correct,
                'incorrect' : incorrect,
                'breakdown':breakdown,
                })
        else:
            test = Test.objects.get(name=request.session['test'])           
            questions, server_answers, total, step_dict = prep_qna(test)

            return render(request, 'quiz/index.html', {
                'form': answerForm(),
                'login_form': loginForm(),
                'child': child,
                'teacher': teacher,
                'test_form': testForm(),
                'questions': questions
                })
    else:
        # this means they are just opening the site on index.

        return render(request, 'quiz/index.html', {
            'login_form': loginForm(),
            'form': answerForm(),
            'test_form': testForm(),
            })

