from django.contrib import admin

from .models import Test, Student, Classroom, Result
# Register your models here.
admin.site.register(Test)
admin.site.register(Student)
admin.site.register(Classroom)
admin.site.register(Result)
