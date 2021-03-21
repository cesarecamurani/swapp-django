# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# import pdb


@login_required
def users_request(request):
    if request.method == 'GET':
        all_users = User.objects.all().order_by('username')
    else:
        all_users = {}

    return render(request, 'users.html', {'all_users': all_users})


@login_required
def user_request(request, username):
    if request.method == 'GET':
        user_details = get_object_or_404(User, username=username)

        return render(request, 'user.html', {'user_details': user_details})
