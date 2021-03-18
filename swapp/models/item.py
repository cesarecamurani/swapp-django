# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
import uuid


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    owner = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)