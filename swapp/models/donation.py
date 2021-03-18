# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from swapp.models import Item
import uuid


class Donation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, editable=False, on_delete=models.PROTECT)
    donor = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    donated_at = models.DateTimeField()
