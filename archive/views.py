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

from dotenv import load_dotenv

load_dotenv()

import os
from openai import OpenAI
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
  api_key=os.environ.get(api_key),
)

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
            thesis = thesis.filter(status='Approved')
        elif search:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search))
            thesis = thesis.filter(status='Approved')
        elif category:
            thesis = ThesisUpload.objects.filter(category=category)
            thesis = thesis.filter(status='Approved')
        else:
            thesis = ThesisUpload.objects.all()
            thesis = thesis.filter(status='Approved')
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
            thesis = thesis.filter(category=category)
            thesis = thesis.filter(status='Approved')
        elif search:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search)).filter(user=request.user)
        elif category:
            thesis = ThesisUpload.objects.filter(category=category).filter(user=request.user)
            thesis = thesis.filter(status='Approved')
        else:
            thesis = ThesisUpload.objects.filter(user=request.user)
            thesis = thesis.filter(status='Approved')
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


@login_required(login_url='login')
def TitleGenerator(request):
    data_response = ""
    if request.method == 'POST':
        category = request.POST.get('title')
        benificiary = request.POST.get('benificiaries')
        generate_number = request.POST.get('generate')

        print(category)
        print(benificiary)
        print(generate_number)


        if generate_number:
            promt = f"create me a {generate_number} example of a capstone title with this categories: {category} for {benificiary}"
        else:
            promt = f"create me example of a capstone title with this categories: {category} for {benificiary}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates Capstone title"},
                {"role": "user", "content": promt}
            ]
            )
        # data_response = response.choices[0].message['content']
        data_response = response.choices[0].message.content
        titles_list = re.split(r'\d+\.\s', data_response)
            # Remove empty strings and strip extra whitespace
        titles_list = [title.strip() for title in titles_list if title.strip()]
        # print(response.choices[0].message.content)
    context = {'ai_return' : titles_list}
    return render(request, 'archive/title_generator.html', context)

def Register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, email=user.email)
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

def Terms(request):
    return render(request, 'archive/termsandconditions.html')