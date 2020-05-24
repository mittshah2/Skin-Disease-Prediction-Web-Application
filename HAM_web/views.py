from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,auth

def home(requests):
    return render(requests,'index.html')

def login(requests):
    return render(requests,'login.html')

def signup(requests):
    if requests.method=='GET':
        return render(requests,'signup.html')
    else:
        name=requests.POST['name']
        username=requests.POST['username']
        password=requests.POST['pass']
        cpassword = requests.POST['cpass']
        age=requests.POST['age']
        blood=requests.POST['blood']
        email=requests.POST['email']

        bg=['O+','O-','B+','B-','A+','A-','AB+','AB-']

        if blood not in bg:
            messages.info(requests, 'Enter a valid blood group')
            return redirect('signup')


        if age.isdigit()==False:
            messages.info(requests, 'Age should be a digit')
            return redirect('signup')

        if name.isalnum():
            messages.info(requests,'Name should contain only alphabets')
            return redirect('signup')
        if(password!=cpassword):
            messages.info(requests,'Both the passwords should match')
            return redirect('signup')
        if(User.objects.filter(username=username).exists()):
            messages.info(requests, 'Username already exists')
            return redirect('signup')

        user=User.objects.create_user(username=username,email=email,password=password,first_name=name)
        user.save()
        user1=auth.authenticate(username=username,password=password)
        if user1 is not None:
            auth.login(requests,user1)
        return redirect('/')

