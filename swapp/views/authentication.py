# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import transaction


@transaction.atomic
def register(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        profile_form = ProfileCreateForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            profile_form = ProfileForm(request.POST, instance=user.profile)  # Reload the profile form with the profile instance
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            profile_form.save()  # Gracefully save the form
    else:
        user_form = UserCreateForm()
        profile_form = ProfileCreateForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
