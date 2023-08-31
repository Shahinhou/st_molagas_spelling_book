from django.shortcuts import redirect,render
from django import forms
import re
from quiz.models import *
from .models import *
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.

class classForm(forms.Form):
    classname = forms.CharField(label="Class Name")

@login_required(login_url='/accounts/login/')
def index(request):

    if request.user.username != 'teacher':
        return redirect("quiz:index") # redirect to your page

    teacher_names = [c.name for c in Classroom.objects.all()]

    if request.method=='POST':

        form = classForm(request.POST)
        if form.is_valid() and request.POST.get('classname') in teacher_names:
            teacher = Classroom.objects.get(name=request.POST.get('classname'))
       
            students = teacher.students.all()
            print(students)

            return render(request, 'grades/index.html', {
                'teacher': teacher,
                'students': students,
                })

        else:
            return render(request,'grades/index.html', {
                'form':classForm()
                })

    else:
        return render(request,'grades/index.html', {
            'form':classForm()
            })



def results(request, student_id):

    child = Student.objects.get(pk=student_id)
    #analysis = child.crit_counter.split('\n')
    
    analysis = child.crit_counter.split('|')
    global_crit = analysis[1].split('\n')
    analysis = analysis[0].split('\n')
    # seperator between global crit and regular crit instead of new model migration.
    
    for i,s in enumerate(analysis):
        a = s.split(',')
        analysis[i] = a

    for i,s in enumerate(global_crit):
        a = s.split(',')
        global_crit[i] = a


    print(global_crit)
    print(analysis)
    

    return render(request, 'grades/results.html', {
        'student': child,
        'analysis': analysis,
        'global_crit': global_crit,
        })




