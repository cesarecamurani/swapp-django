# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import pdb

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, 'layout.html')
