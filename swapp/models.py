# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=30)


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    owner = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)


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


class Donations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, editable=False, on_delete=models.PROTECT)
    donor = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    donated_at = models.DateTimeField()

