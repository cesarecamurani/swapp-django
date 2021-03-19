# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import transaction
from django.shortcuts import render

from swapp.forms import UserCreateForm, ProfileCreateForm


@transaction.atomic
def register(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        profile_form = ProfileCreateForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            profile_form = ProfileCreateForm(request.POST, instance=user.profile)
            profile_form.full_clean()
            profile_form.save()
    else:
        user_form = UserCreateForm()
        profile_form = ProfileCreateForm()

    return render(request, 'register.djt', {
        'user_form': user_form,
        'profile_form': profile_form
    })
