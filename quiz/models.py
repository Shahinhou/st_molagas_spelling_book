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
    f5 = 'static/text/crit_to_step.txt'
    
    name = models.CharField(max_length=100,default="unnamed_test")
    questions = models.TextField(default=write_text(str(f4)))
    crit_list = models.TextField(default=write_text(str(f1)))
    unique_crits = models.TextField(default=write_text(str(f2)))
    regs = models.TextField(default=write_text(str(f3)))
    steps = models.TextField(default='nothing')
    other_crit = models.TextField(default='nothing')

    def __str__(self):
        return self.name

class Student(models.Model):

    name = models.CharField(max_length=100,default="john")
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)
    breakdown = models.TextField(max_length=500000,default="none")
    crit_counter = models.TextField(max_length=500000,default="none")
    

    #classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="student")
    result_sheet = RichTextField(max_length=500000, default="none")

    def __str__(self):
        return self.name

class Classroom(models.Model):

    name = models.CharField(max_length=100, default="Ms. de Faoite")
    #text = models.TextField(max_length=500000, default="hello world")
    # foreign key list?
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name

