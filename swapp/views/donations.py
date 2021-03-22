# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pdb
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
# from django.contrib import messages
from django.shortcuts import render

from swapp.models import Donation, Item


@login_required
@transaction.atomic
def donations_request(request):
    if request.method == 'POST':
        donation = Donation()
        item_id = request.POST['item_id']
        donation.item_id = item_id
        donation.donor_id = request.user.id
        donation.donated_at = datetime.now()
        donation.save()

        item = Item.objects.filter(id=item_id)[0]
        item.donated = True
        item.save()

        all_donations = Donation.objects.all().order_by('donated_at')
    elif request.method == 'GET':
        all_donations = Donation.objects.all().order_by('donated_at')
    else:
        all_donations = []

    return render(request, 'donations.html', {'all_donations':  all_donations})
