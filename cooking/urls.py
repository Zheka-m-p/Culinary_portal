from django.urls import path
from . import views

app_name='cooking'

urlpatterns = [
    path('', views.index, name='index'),
]