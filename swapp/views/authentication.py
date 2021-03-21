# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
import pdb
from swapp.forms import UserCreateForm, ProfileCreateForm, UserLoginForm


@transaction.atomic
def register_request(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        profile_form = ProfileCreateForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            user.refresh_from_db()
            profile_form = ProfileCreateForm(request.POST, instance=user.profile)
            profile_form.full_clean()
            profile_form.save()

            return redirect('/')

        messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        user_form = UserCreateForm()
        profile_form = ProfileCreateForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@transaction.atomic
def login_request(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                messages.info(request, f'You are now logged in as {username}.')

                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'login_form': form})


@transaction.atomic
def logout_request(request):
    logout(request)
    messages.info(request, 'You\'ve been successfully logged out.')
    return redirect('login')
