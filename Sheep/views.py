# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
def login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                messages.success(request,"Login successfully.")
                return redirect("/")
            else:
                messages.warning(request,"User not validated.")
                return redirect("/account/login")
        else:
            messages.warning(request,"Username or password failed.")
            return redirect("/account/login")
    return render(request, 'Sheep/login.html')

def logout_view(request):
    logout(request)
    messages.success(request,"Log out successfully.")
    return redirect("/")

def signup(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, password=password)
            user.save()
        except IntegrityError as e: 
            messages.warning(request,"Try another username.")
            return redirect("/account/signup")
        messages.success(request,"Sign up successfully.")
        return redirect("/account/login")
    else:
        return render(request, 'Sheep/signup.html')