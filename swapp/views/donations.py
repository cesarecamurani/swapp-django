# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.contrib.auth.decorators import login_required
# from django.db import transaction
# from django.contrib import messages
# from django.shortcuts import render, redirect
#
#
# @login_required
# @transaction.atomic
# def donations(request):
#     if request.method == 'POST':
#         donations_form = DonationsCreateForm(request.POST)
#
#         if donations_form.is_valid():
#             donation = donations_form.save(commit=False)
#             donation.save()
#
#             messages.success(request, 'Donation successful. Thank you very much!')
#
#             return redirect('/')
#
#         messages.error(request, 'Unsuccessful donation. Invalid information.')
#     else:
#         donations_form = DonationsCreateForm()
#
#     return render(request, 'donations.html', {
#         'donations_form': donations_form
#     })
