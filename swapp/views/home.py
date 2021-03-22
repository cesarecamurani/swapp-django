# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import pdb

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect


@login_required
@transaction.atomic
def index(request):
    return redirect('items')
