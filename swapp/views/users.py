# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import HttpResponseRedirect
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

            pending_sent_swapp_requests = sent_swapp_requests.filter(state='IN')
            pending_received_swapp_requests = received_swapp_requests.filter(state='IN')

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
        else:
            user_items = []
            pending_sent_swapp_requests = []
            pending_received_swapp_requests = []
            closed_swapp_requests = []
            # page_obj = None

            messages.error(request, 'Swapper not found!')

        return render(request, 'user.html', {
            'user_details': user_details,
            'user_items': user_items,
            'sent_swapp_requests': pending_sent_swapp_requests,
            'received_swapp_requests': pending_received_swapp_requests,
            'closed_swapp_requests': closed_swapp_requests,
            # 'page_obj': page_obj
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

            offered_item.owner = request.user
            offered_item.out_for_request = False
            offered_item.save()

            requested_item.owner = offerer
            requested_item.save()

            same_item_requests = SwappRequest.objects.all().filter(
                requested_product=swapp_request_details.requested_product
            ).exclude(pk=swapp_request_details.id)

            for req in same_item_requests:
                req.state = 'RJ'
                req.save()
                req.offered_product.out_for_request = False
                req.offered_product.save()

            messages.info(
                request,
                'You accepted Swapp Request with Trace ID {}.'.format(swapp_request_details.trace_id)
            )

            return HttpResponseRedirect(
                '/users/{}/swapp_requests/{}'.format(
                    request.user.username, swapp_request_details.trace_id
                )
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
            offered_item.out_for_request = False
            offered_item.save()

            messages.error(
                request,
                'You rejected Swapp Request with Trace ID {}.'.format(swapp_request_details.trace_id)
            )

            return HttpResponseRedirect(
                '/users/{}/swapp_requests/{}'.format(
                    request.user.username, swapp_request_details.trace_id
                )
            )


def __swapp_request_state(db_state):
    states = {
        'IN': 'Initial',
        'AC': 'Accepted',
        'RJ': 'Rejected',
    }
    return states.get(db_state, '')
