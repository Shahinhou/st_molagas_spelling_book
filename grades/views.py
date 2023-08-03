from django.shortcuts import render
from django import forms
import re
from quiz.models import *
from .models import *
import datetime
# Create your views here.

class classForm(forms.Form):
    classname = forms.CharField(label="Class Name")

def index(request):

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
    analysis = child.crit_counter.split('\n')
    

    return render(request, 'grades/results.html', {
        'student': child,
        'analysis': analysis,
        })




