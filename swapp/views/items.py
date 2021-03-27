# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from swapp.forms import ItemCreateForm, SwappRequestCreateForm
from swapp.models import Item, SwappRequest
import pdb


@login_required
@transaction.atomic
def items_request(request):
    if request.method == 'GET':
        all_items = Item.objects.all().filter(donated=False).order_by('-created_at')
    elif request.method == 'POST':
        query = request.POST['search']
        all_items = Item.objects.filter(name__icontains=query)
    else:
        all_items = []

    return render(request, 'items.html', {'all_items': all_items})


@login_required
@transaction.atomic
def item_request(request, item_id):
    if request.method == 'GET':
        item_details = get_object_or_404(Item, pk=item_id)

        return render(request, 'item.html', {'item_details': item_details})


@login_required
@transaction.atomic
def item_delete_request(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=item_id)
        item.delete()

        return HttpResponseRedirect('/users/{}'.format(request.user.username))

    return render(request, 'user.html')


@login_required
@transaction.atomic
def item_create_request(request):
    if request.method == 'POST':
        item_form = ItemCreateForm(request.POST, request.FILES)

        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.owner = get_object_or_404(User, pk=request.user.id)
            item.created_at = datetime.now()
            item.save()
            messages.success(request, 'Item uploaded successfully.')

            return redirect('/')

        messages.error(request, 'Unsuccessful uploading. Invalid information.')
    else:
        item_form = ItemCreateForm()

    return render(request, 'add_item.html', {
        'item_form': item_form
    })


@login_required
@transaction.atomic
def new_swapp_request(request, item_id):
    user = request.user
    items = user.item_set.all().filter(donated=False, out_for_request=False)

    if request.method == 'POST':
        swapp_request_form = SwappRequestCreateForm(request.POST, user=user)

        if swapp_request_form.is_valid():
            swapp_request = swapp_request_form.save(commit=False)

            offered_product_id = request.POST['offered_product']
            swapp_request.offered_product = get_object_or_404(Item, pk=offered_product_id)
            swapp_request.requested_product = get_object_or_404(Item, pk=item_id)
            swapp_request.offered_product_owner_id = user.id
            swapp_request.requested_product_owner_id = swapp_request.requested_product.owner_id
            swapp_request.trace_id = __generate_trace_id()
            swapp_request.save()

            offered_item = swapp_request.offered_product
            offered_item.out_for_request = True
            offered_item.save()

            messages.success(request, 'Swapp request sent successfully.')

            return redirect('/')

        messages.error(request, 'Unsuccessful swapp request. Invalid information.')
    else:
        swapp_request_form = SwappRequestCreateForm(user=user)

    return render(request, 'new_swapp_request.html', {
        'swapp_request_form': swapp_request_form,
        'items': items
    })


def __generate_trace_id():
    return 'SWP-' + ''.join(
        random.choices(
            string.ascii_uppercase + string.digits, k=16
        )
    )
