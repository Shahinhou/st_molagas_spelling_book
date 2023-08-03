from django.db import models
from ckeditor.fields import RichTextField
from . import make_hashmap
from django.utils.html import strip_tags
# Create your models here.

# how to def __str__

def making_maps():

    f1 = 'static/text/no_bracket_criteria.txt'
    f2 = 'static/text/unique_criteria.txt'
    f3 = 'static/text/regex_expressions.txt'
    
    d1 = make_map(f1)
    d2 = make_eng_to_regex(f2, f3)

class Test(models.Model):

    # writer = models.ForeignKey(Writer, on_delete=models.CASCADE, related_name="works")
    def build_map(f1, f2, f3): 
        word_to_crit = make_hashmap.make_map(f1)
        crit_to_reg = make_hashmap.make_eng_to_regex(f2, f3)

    def write_text(f1):

        with open(f1) as f:
            text = [c.strip() for c in f.readlines()]
            text = '\n'.join(text)
        
        return text
    
    word_to_crit = {}
    crit_to_reg = {}

    # would like a way to make these a CharField()...
    
    f1 = 'static/text/no_bracket_criteria.txt'
    f2 = 'static/text/unique_criteria_list.txt'
    f3 = 'static/text/regex_expressions.txt'
    f4 = 'static/text/testsheet.txt'

    questions = models.TextField(default=write_text(str(f4)))
    crit_list = models.TextField(default=write_text(str(f1)))
    unique_crits = models.TextField(default=write_text(str(f2)))
    regs = models.TextField(default=write_text(str(f3)))

class Classroom(models.Model):

    name = models.CharField(max_length=100, default="Ms. de Faoite")
    # foreign key list?
    students = []

class Student(models.Model):

    name = models.CharField(max_length=100,default="john")
    password = models.CharField(max_length=100, default='1234')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="student")

class Result(models.Model):

    test = models.ForeignKey(Test, on_delete=models.CASCADE,related_name="result")
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name="result")
    result_sheet = models.TextField(max_length=500000, default="none")
