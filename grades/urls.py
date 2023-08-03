from django.urls import include,path
from . import views

app_name = 'grades'

urlpatterns = [
        path('', views.index, name='index'),
        path("results/<int:student_id>/",views.results, name='results')
        ]
