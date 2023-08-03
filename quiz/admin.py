from django.contrib import admin

from .models import Test, Student, Classroom
# Register your models here.
admin.site.register(Test)
admin.site.register(Student)
admin.site.register(Classroom)
