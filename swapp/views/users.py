# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pdb

from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from swapp.forms import ChangePasswordForm, ProfileCreateForm, UserUpdateForm
from swapp.models import SwappRequest, Donation
from notifications.signals import notify


@login_required
@transaction.atomic
def users_request(request):
    if request.method == 'GET':
        all_users = User.objects.all().exclude(username='cesarecamurani').order_by('username')
    elif request.method == 'POST':
        query = request.POST['search']
        all_users = User.objects.filter(username__istartswith=query)
    else:
        all_users = []

    page = request.GET.get('page', 1)
    paginator = Paginator(all_users, 10)

    try:
        all_users = paginator.page(page)
    except PageNotAnInteger:
        all_users = paginator.page(1)
    except EmptyPage:
        all_users = paginator.page(paginator.num_pages)

    return render(request, 'users.html', {'all_users': all_users})


@login_required
@transaction.atomic
def user_request(request, username):
    if request.method == 'GET':
        user_details = get_object_or_404(User, username=username)

        if user_details:
            user_items = user_details.item_set.all().filter(donated=False, removed=False).order_by('-created_at')
            sent_swapp_requests = SwappRequest.objects.all().filter(offered_product_owner_id=user_details.id)
            received_swapp_requests = SwappRequest.objects.all().filter(requested_product_owner_id=user_details.id)

            pending_sent_swapp_requests = sent_swapp_requests.filter(state='IN').order_by('-closed_at')
            pending_received_swapp_requests = received_swapp_requests.filter(state='IN').order_by('-closed_at')

            closed_sent_swapp_requests = sent_swapp_requests.filter(state__in=['AC', 'RJ'])
            closed_received_swapp_requests = received_swapp_requests.filter(state__in=['AC', 'RJ'])

            closed_swapp_requests = (closed_sent_swapp_requests | closed_received_swapp_requests).order_by('-closed_at')

            page = request.GET.get('page', 1)
            paginator = Paginator(closed_swapp_requests, 10)

            try:
                closed_swapp_requests = paginator.page(page)
            except PageNotAnInteger:
                closed_swapp_requests = paginator.page(1)
            except EmptyPage:
                closed_swapp_requests = paginator.page(paginator.num_pages)

            page = request.GET.get('page', 1)
            paginator = Paginator(pending_sent_swapp_requests, 10)

            try:
                pending_sent_swapp_requests = paginator.page(page)
            except PageNotAnInteger:
                pending_sent_swapp_requests = paginator.page(1)
            except EmptyPage:
                pending_sent_swapp_requests = paginator.page(paginator.num_pages)

            page = request.GET.get('page', 1)
            paginator = Paginator(pending_received_swapp_requests, 10)

            try:
                pending_received_swapp_requests = paginator.page(page)
            except PageNotAnInteger:
                pending_received_swapp_requests = paginator.page(1)
            except EmptyPage:
                pending_received_swapp_requests = paginator.page(paginator.num_pages)

        else:
            user_items = []
            pending_sent_swapp_requests = []
            pending_received_swapp_requests = []
            closed_swapp_requests = []

            messages.error(request, 'Swapper not found!')

        return render(request, 'user.html', {
            'user_details': user_details,
            'user_items': user_items,
            'sent_swapp_requests': pending_sent_swapp_requests,
            'received_swapp_requests': pending_received_swapp_requests,
            'closed_swapp_requests': closed_swapp_requests
        })


@login_required
@transaction.atomic
def update_profile_request(request, username):
    if request.method == 'POST':
        update_user_form = UserUpdateForm(request.POST)
        update_profile_form = ProfileCreateForm(request.POST)

        if update_user_form.is_valid() and update_profile_form.is_valid():
            update_user_form = UserUpdateForm(request.POST, instance=request.user)
            update_user_form.full_clean()
            update_user_form.save()

            update_profile_form = ProfileCreateForm(request.POST, instance=request.user.profile)
            update_profile_form.full_clean()
            update_profile_form.save()

            notify.send(request.user, recipient=request.user, verb='Profile updated successfully.')

            messages.success(request, 'Profile updated successfully.')

            return redirect(f'/users/{request.user.username}')

        messages.error(request, 'Unsuccessful update. Invalid information.')
    else:
        update_user_form = UserUpdateForm(instance=request.user)
        update_profile_form = ProfileCreateForm(instance=request.user.profile)

    return render(request, 'update_profile.html', {
        'update_user_form': update_user_form,
        'update_profile_form': update_profile_form
    })


@login_required
@transaction.atomic
def delete_user_request(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        sent_swapp_requests = SwappRequest.objects.all().filter(offered_product_owner_id=user.id)
        received_swapp_requests = SwappRequest.objects.all().filter(requested_product_owner_id=user.id)

        initial_sent_swapp_requests = sent_swapp_requests.filter(state='IN')
        closed_sent_swapp_requests = sent_swapp_requests.filter(state__in=['AC', 'RJ'])

        initial_received_swapp_requests = received_swapp_requests.filter(state='IN')
        closed_received_swapp_requests = received_swapp_requests.filter(state__in=['AC', 'RJ'])

        for req in initial_sent_swapp_requests:
            offered_item = req.offered_product
            requested_item = req.requested_product
            recipient = requested_item.owner

            notify.send(
                recipient,
                recipient=recipient,
                verb=f'The request to swapp {offered_item.name} for {requested_item.name} has been canceled because the owner '
                     f'deleted their account. '
                     f'The request with ID {req.trace_id} is no longer visible to you and won\'t be displayed '
                     f'in your History.'
            )
            req.delete()

        for req in initial_received_swapp_requests:
            offered_item = req.offered_product
            requested_item = req.requested_product
            recipient = offered_item.owner

            offered_item.out_for_request = False
            offered_item.save()

            notify.send(
                recipient,
                recipient=recipient,
                verb=f'The request to swapp {offered_item.name} for {requested_item.name} has been canceled because the owner '
                     f'deleted their account. '
                     f'The request with ID {req.trace_id} is no longer visible to you and won\'t be displayed '
                     f'in your History.'
            )
            req.delete()

        for req in closed_sent_swapp_requests:
            if req.state == 'AC':
                recipient = req.offerred_product.owner
            else:
                recipient = req.requested_product.owner

            notify.send(
                recipient,
                recipient=recipient,
                verb=f'The request with ID {req.trace_id} is no longer visible to you and won\'t be displayed '
                     f'in your History because the other party deleted their account.'

            )
            req.delete()

        for req in closed_received_swapp_requests:
            if req.state == 'AC':
                recipient = req.requested_product.owner
            else:
                recipient = req.offered_product.owner

            notify.send(
                recipient,
                recipient=recipient,
                verb=f'The request with ID {req.trace_id} is no longer visible to you and won\'t be displayed '
                     f'in your History because the other party deleted their account.'

            )
            req.delete()

        user_donations = Donation.objects.all().filter(donor=user)

        for donation in user_donations:
            donation.donor = get_object_or_404(User, username='cesarecamurani')
            donation.save()

        messages.error(request, 'You\'ve successfully deleted your account. Sorry to see you go!')

        user.delete()

        logout(request)

        return redirect('login')
    else:
        return render(request, 'delete_account.html')


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

                notify.send(user, recipient=user, verb='Password changed successfully.')

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
            requested_item_owner = get_object_or_404(User, pk=swapp_request_details.requested_product_owner_id)
            request_state = __swapp_request_state(swapp_request_details.state)
        else:
            offered_item = None
            requested_item = None
            offerer = None
            requested_item_owner = None
            request_state = ''

        return render(request, 'swapp_request.html', {
            'swapp_request_details': swapp_request_details,
            'offered_item': offered_item,
            'requested_item': requested_item,
            'offerer': offerer,
            'requested_item_owner': requested_item_owner,
            'user': request.user,
            'request_state': request_state
        })


@login_required
@transaction.atomic
def accept_swapp_request(request, username, trace_id):
    if request.method == 'POST':
        swapp_request_details = get_object_or_404(SwappRequest, trace_id=trace_id)

        if swapp_request_details:
            swapp_request_details.state = 'AC'
            swapp_request_details.save()

            offered_item = swapp_request_details.offered_product
            requested_item = swapp_request_details.requested_product
            user_id = swapp_request_details.offered_product_owner_id
            offerer = get_object_or_404(User, pk=user_id)

            notify.send(
                offerer,
                recipient=offerer,
                verb=f'Your request to swapp {offered_item.name} for {requested_item.name} has been accepted. '
                     f'You can find the details in your History, in the request with ID {swapp_request_details.trace_id}'
            )

            offered_item.owner = request.user
            offered_item.out_for_request = False
            offered_item.current_location = ''
            offered_item.preferred_change = ''
            offered_item.save()

            requested_item.owner = offerer
            requested_item.current_location = ''
            requested_item.preferred_change = ''
            requested_item.save()

            same_offered_item_requests = SwappRequest.objects.all().filter(
                requested_product=swapp_request_details.offered_product
            ).exclude(pk=swapp_request_details.id, state__in=['AC', 'RJ'])

            same_requested_item_requests = SwappRequest.objects.all().filter(
                requested_product=swapp_request_details.requested_product
            ).exclude(pk=swapp_request_details.id, state__in=['AC', 'RJ'])

            all_same_item_requests = same_offered_item_requests | same_requested_item_requests

            for req in all_same_item_requests:
                req.state = 'RJ'
                req.save()
                req.offered_product.out_for_request = False
                req.offered_product.save()

                notify.send(
                    req.offered_product.owner,
                    recipient=req.offered_product.owner,
                    verb=f'Your request to swapp {req.offered_product.name} for {req.requested_product.name} has been rejected. '
                         f'You can find the details in your History, in the request with ID {req.trace_id}'
                )

            messages.info(
                request,
                f'You accepted Swapp Request with Trace ID {swapp_request_details.trace_id}.'
            )

            return HttpResponseRedirect(
                f'/users/{request.user.username}/swapp_requests/{swapp_request_details.trace_id}'
            )


@login_required
@transaction.atomic
def reject_swapp_request(request, username, trace_id):
    if request.method == 'POST':
        swapp_request_details = get_object_or_404(SwappRequest, trace_id=trace_id)

        if swapp_request_details:
            swapp_request_details.state = 'RJ'
            swapp_request_details.save()

            offered_item = swapp_request_details.offered_product
            requested_item = swapp_request_details.requested_product

            offered_item.out_for_request = False
            offered_item.save()

            user = get_object_or_404(User, pk=swapp_request_details.offered_product_owner_id)

            notify.send(
                user,
                recipient=user,
                verb=f'Your request to swapp {offered_item.name} for {requested_item.name} has been rejected. '
                     f'You can find the details in your History, in the request with ID {swapp_request_details.trace_id}'
            )

            messages.error(
                request,
                f'You rejected Swapp Request with Trace ID {swapp_request_details.trace_id}.'
            )

            return HttpResponseRedirect(
                f'/users/{request.user.username}/swapp_requests/{swapp_request_details.trace_id}'
            )


@login_required
@transaction.atomic
def delete_swapp_request(request, username, trace_id):
    if request.method == 'POST':
        swapp_request_obj = get_object_or_404(SwappRequest, trace_id=trace_id)
        swapp_request_obj.delete()

        messages.error(request, f'You\'ve successfully deleted the request with trace ID {swapp_request_obj.trace_id}')

        offered_item = swapp_request_obj.offered_product
        requested_item = swapp_request_obj.requested_product
        recipient = requested_item.owner

        offered_item.out_for_request = False
        offered_item.save()

        notify.send(
            recipient,
            recipient=recipient,
            verb=f'The request to swapp {offered_item.name} for {requested_item.name} has been canceled by its owner. '
                 f'The request with ID {swapp_request_obj.trace_id} is no longer visible to you and won\'t be displayed '
                 f'in your History.'
        )

        return HttpResponseRedirect(f'/users/{request.user.username}')


def __swapp_request_state(db_state):
    states = {
        'IN': 'Initial',
        'AC': 'Accepted',
        'RJ': 'Rejected',
    }
    return states.get(db_state, '')
