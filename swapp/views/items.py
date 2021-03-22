# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime

from django.db import transaction
from django.http import HttpResponseRedirect

from swapp.forms import ItemCreateForm
from swapp.models import Item
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import pdb


@login_required
@transaction.atomic
def items_request(request):
    if request.method == 'GET':
        all_items = Item.objects.all().filter(donated=False).order_by('created_at')
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

        return render(request, 'user.html', {'item_details': item_details})


@login_required
@transaction.atomic
def item_delete_request(request, item_id):
    # pdb.set_trace()
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=item_id)
        item.delete()

        return HttpResponseRedirect('/users/{}'.format(request.user.username))

    return render(request, 'user.html')


@login_required
@transaction.atomic
def item_create_request(request):
    if request.method == 'POST':
        item_form = ItemCreateForm(request.POST)

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
