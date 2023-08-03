from django.shortcuts import render
from django import forms
import re
from quiz.models import *
from .models import *
import datetime
# Create your views here.

def index(request):

    teacher = Classroom.objects.get(name='jane')
    students = teacher.students.all()
    print(students)

    return render(request, 'grades/index.html', {
        'teacher': teacher,
        'students': students,
        })

def results(request, student_id):

    child = Student.objects.get(pk=student_id)
    analysis = []

    for lines in child.crit_counter:
        lines = lines.strip()
        analysis.append(lines)

    return render(request, 'grades/results.html', {
        'student': child,
        'analysis': analysis,
        })
