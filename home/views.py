from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
import matplotlib.pyplot as p
import numpy as np
import cv2
from .models import pics
from PIL import Image
from tensorflow.keras.models import load_model
import os

def home(requests):
    if requests.method=='GET':
        params={'disp':False}
        return render(requests,'index.html',params)
    else:
        img=requests.FILES['img']
        obj=pics.objects.create(img=img)
        image=Image.open(obj.img)
        image=image.resize((135,180))
        image=np.array(image)
        image=np.expand_dims(image,axis=0)
        base=os.getcwd()
        path=os.path.join(os.path.join(base,'home'),'static_home')
        path=os.path.join(path,'model.h5')
        model=load_model(path)
        pred=model.predict_classes(image)[0]
        label = {
            0:'Actinic keratoses',
            1:'Basal cell carcinoma',
            2:'Benign keratosis-like lesions',
            3:'Dermatofibroma',
            4:'Melanocytic nevi',
            5:'Melanoma',
            6:'Vascular lesions'
        }
        disease=label[pred]
        params={'disease':disease,'disp':True}

        return render(requests,'index.html',params)


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

        if name.isalpha()==False:
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


def login(requests):
    if requests.method == 'GET':
        return render(requests, 'login.html')
    else:
        username=requests.POST['uname']
        password=requests.POST['pass']
        user1 = auth.authenticate(username=username, password=password)
        if user1 is not None:
            auth.login(requests, user1)
            return redirect('/')
        else:
            messages.info(requests,'Invalid credentials')
            return redirect('login')

def logout(requests):
    auth.logout(requests)
    return redirect('/')


