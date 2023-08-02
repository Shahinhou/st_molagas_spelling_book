from django.contrib import admin

from .models import Test, uniqueCriteria, regForCriteria, wordToCriteria
# Register your models here.
admin.site.register(Test)
admin.site.register(uniqueCriteria)
admin.site.register(regForCriteria)
admin.site.register(wordToCriteria)
