# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _
from django.db import models
from swapp.models import Item
import uuid


class SwappRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    offered_product = models.ForeignKey(Item, related_name='offered_product_id', editable=False, on_delete=models.CASCADE)
    requested_product = models.ForeignKey(Item, related_name='requested_product_id', editable=False, on_delete=models.CASCADE)
    offered_product_owner_id = models.UUIDField(default=uuid.uuid4, editable=False)
    requested_product_owner_id = models.UUIDField(default=uuid.uuid4, editable=False)

    class Status(models.TextChoices):
        INITIAL = 'IN', _('Initial')
        ACCEPTED = 'AC', _('Accepted')
        REJECTED = 'RJ', _('Rejected')

    state = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.INITIAL
    )
