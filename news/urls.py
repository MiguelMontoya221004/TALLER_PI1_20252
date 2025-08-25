# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name='news'),   # esta es la vista principal de noticias
]
