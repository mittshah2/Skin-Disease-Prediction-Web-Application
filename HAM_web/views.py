from django.shortcuts import render
from django.http import HttpResponse

def home(requests):
    return render(requests,'index.html')

def login(requests):
    return render(requests,'login.html')

def signup(requests):
    return render(requests,'signup.html')