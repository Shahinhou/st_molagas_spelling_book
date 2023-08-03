from django.urls import include,path
from . import views

app_name = 'quiz'

urlpatterns = [
        path('', views.index, name='index'),
        ]
