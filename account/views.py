from account.models import CustomUser
from django.db import reset_queries
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login , logout
from django.urls.base import reverse 
from .forms import *
import httpagentparser


def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            next_ = request.GET.get('next')
            if next_:
                return redirect(next_)
            return redirect(reverse('index'))
        else:
            error = "Username or password invalid"
    
    context = {'error':error}

    return render(request,'account/login.html',context)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            ip = get_client_ip(request)
            os = httpagentparser.detect(request.META["HTTP_USER_AGENT"])['os']
            os = os['name'] + "-"+os['version']
            user = CustomUser.objects.create_user(username=username,password=password,ip=ip,os=os)
            login(request,user)
            return redirect(reverse('index'))
    
    context = {'form':form}
    return render(request,'account/register.html',context)
    

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))