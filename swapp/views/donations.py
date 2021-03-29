# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from notifications.signals import notify

from swapp.models import Donation, Item, SwappRequest


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
        item_swapp_requests = SwappRequest.objects.all().filter(requested_product=item)

        for req in item_swapp_requests:
            req.state = 'RJ'
            req.save()
            req.offered_product.out_for_request = False
            req.offered_product.save()

            notify.send(
                req.offered_product.owner,
                recipient=req.offered_product.owner,
                verb=f'Your request to swapp your {req.offered_product.name} for {req.requested_product.name} has been automatically rejected '
                     f'because the item you requested has been donated to the site\'s charity by its owner. '
                     f'You can find the details in your History, in the request with ID {req.trace_id}'
            )

        item.owner = get_object_or_404(User, username='cesarecamurani')
        item.donated = True
        item.save()

        return HttpResponseRedirect('/donations')

    elif request.method == 'GET':
        all_donations = Donation.objects.all().order_by('-donated_at')
    else:
        all_donations = []

    page = request.GET.get('page', 1)
    paginator = Paginator(all_donations, 10)

    try:
        all_donations = paginator.page(page)
    except PageNotAnInteger:
        all_donations = paginator.page(1)
    except EmptyPage:
        all_donations = paginator.page(paginator.num_pages)

    return render(request, 'donations.html', {'all_donations':  all_donations})
