from calendar import c
from dataclasses import is_dataclass
from lib2to3.pgen2 import driver
from multiprocessing import context
from operator import inv
import re
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from pytz import timezone

from django.http import JsonResponse

import requests 
from django.db.models import Q

from .models import *
from .forms import *

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required(login_url='login')
def Home(request):
    thesis = ThesisUpload.objects.all()
    categories = ThesisUpload.objects.values("category").distinct()
    print(categories)
    if request.method == 'POST':
        search = request.POST.get('search')
        category = request.POST.get('category')
        print(search, category)
        if search and category:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search))
            print(thesis)
            thesis = thesis.filter(category=category)
            print(thesis)
        elif search:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search))
        elif category:
            thesis = ThesisUpload.objects.filter(category=category)
        else:
            thesis = ThesisUpload.objects.all()
    context = {'thesis': thesis, 'category': categories}
    return render(request, 'archive/thesis_archive.html', context)

@login_required(login_url='login')
def ThesisUploadPage(request):
    thesis = ThesisUpload.objects.all()
    form = ThesisForm()
    if request.method == 'POST':
        form = ThesisForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()
            return redirect('home')
    context = {'thesis': thesis}
    return render(request, 'archive/upload_thesis.html', context)

@login_required(login_url='login')
def MyUploads(request):
    thesis = ThesisUpload.objects.filter(user=request.user)
    categories = ThesisUpload.objects.values("category").distinct()
    print(categories)
    if request.method == 'POST':
        search = request.POST.get('search')
        category = request.POST.get('category')
        print(search, category)
        if search and category:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search)).filter(user=request.user)
            print(thesis)
            thesis = thesis.filter(category=category)
            print(thesis)
        elif search:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search)).filter(user=request.user)
        elif category:
            thesis = ThesisUpload.objects.filter(category=category).filter(user=request.user)
        else:
            thesis = ThesisUpload.objects.filter(user=request.user)
    context = {'thesis': thesis, 'category': categories}
    return render(request, 'archive/user_uploads.html', context)

@login_required(login_url='login')
def ProfilePage(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print(form.errors)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()
            return redirect('profile')
    context = {'form': form, 'profile': profile}
    return render(request, 'archive/profile.html', context)

@login_required(login_url='login')
def CompareResearch(request):
    return render(request, 'archive/compare.html')

def Register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')
    context = {'form': form}
    return render(request, 'archive/register.html', context)

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect') 
    return render(request, 'archive/login.html')

def Logout(request):
    logout(request)
    return redirect('login')


def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'archive/change_password.html', {
        'form': form
    })