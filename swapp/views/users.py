# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
import pdb

from swapp.forms import ChangePasswordForm
from swapp.models import SwappRequest, Item


@login_required
@transaction.atomic
def users_request(request):
    if request.method == 'GET':
        all_users = User.objects.all().order_by('username')
    elif request.method == 'POST':
        query = request.POST['search']
        all_users = User.objects.filter(username__istartswith=query)
    else:
        all_users = []

    return render(request, 'users.html', {'all_users': all_users})


@login_required
@transaction.atomic
def user_request(request, username):
    if request.method == 'GET':
        user_details = get_object_or_404(User, username=username)

        if user_details:
            user_items = user_details.item_set.all().filter(donated=False)
            sent_swapp_requests = SwappRequest.objects.all().filter(offered_product_owner_id=user_details.id)
            received_swapp_requests = SwappRequest.objects.all().filter(requested_product_owner_id=user_details.id)
        else:
            user_items = []
            sent_swapp_requests = []
            received_swapp_requests = []
            messages.error(request, 'Swapper not found!')

        return render(request, 'user.html', {
            'user_details': user_details,
            'user_items': user_items,
            'sent_swapp_requests': sent_swapp_requests,
            'received_swapp_requests': received_swapp_requests
        })


@login_required
@transaction.atomic
def change_password_request(request, username):
    if request.method == 'POST':
        password_form = ChangePasswordForm(request.POST)

        if password_form.is_valid():
            password = password_form.cleaned_data.get('old_password')
            new_password = password_form.cleaned_data.get('new_password')

            user = authenticate(username=username, password=password)

            if user is not None:
                user.set_password(new_password)
                user.save()

                messages.info(request, 'Password changed successfully.')

                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        password_form = ChangePasswordForm()

    return render(request, 'registration/change_password.html', {'password_form': password_form})


@login_required
@transaction.atomic
def swapp_request(request, username, trace_id):
    if request.method == 'GET':
        swapp_request_details = get_object_or_404(SwappRequest, trace_id=trace_id)

        if swapp_request_details:
            offered_item = swapp_request_details.offered_product
            requested_item = swapp_request_details.requested_product
            user_id = swapp_request_details.offered_product_owner_id
            offerer = get_object_or_404(User, pk=user_id)
            user = get_object_or_404(User, username=username)
        else:
            offered_item = None
            requested_item = None
            offerer = None
            user = None

        return render(request, 'swapp_request.html', {
            'swapp_request_details': swapp_request_details,
            'offered_item': offered_item,
            'requested_item': requested_item,
            'offerer': offerer,
            'user': user
        })
