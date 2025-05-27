# main_app/views.py

from django.shortcuts import render
from django.http import HttpResponse

# home view function
def home(req):
    return HttpResponse('<h1>hi</h1>')

def about(req):
    return HttpResponse('<h1>about</h1>')