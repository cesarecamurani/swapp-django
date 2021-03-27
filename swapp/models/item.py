# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
import uuid


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    donated = models.BooleanField(default=False)
    out_for_request = models.BooleanField(default=False)
    picture = models.FileField(upload_to='pictures', default='')
    preferred_change = models.CharField(max_length=15, default='')
    current_location = models.CharField(max_length=15, default='')
    owner = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)
