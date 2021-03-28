# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from notifications.models import Notification


@login_required
@transaction.atomic
def notifications_request(request, username):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username)
        all_notifications = Notification.objects.all().filter(actor_object_id=user.id).order_by('-timestamp')
        unread_notifications = all_notifications.filter(unread=True)
        unread_notifications_count = len(unread_notifications)

        return render(request, 'notifications.html', {
            'all_notifications': all_notifications,
            'unread_notifications': unread_notifications,
            'unread_notifications_count': unread_notifications_count
        })


@login_required
@transaction.atomic
def mark_as_read_request(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=notification_id)
        notification.unread = False
        notification.save()

        return HttpResponseRedirect(f'/users/{request.user.username}/notifications')

    return render(request, 'notifications.html')


@login_required
@transaction.atomic
def mark_all_as_read_request(request):
    if request.method == 'POST':
        notifications = Notification.objects.all().filter(actor_object_id=request.user.id)

        for notification in notifications:
            notification.unread = False
            notification.save()

        return HttpResponseRedirect(f'/users/{request.user.username}/notifications')


@login_required
@transaction.atomic
def delete_notification_request(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=notification_id)
        notification.delete()

        return HttpResponseRedirect(f'/users/{request.user.username}/notifications')

    return render(request, 'notifications.html')


@login_required
@transaction.atomic
def delete_all_notifications_request(request):
    if request.method == 'POST':
        notifications = Notification.objects.all().filter(actor_object_id=request.user.id)

        for notification in notifications:
            notification.delete()

        return HttpResponseRedirect(f'/users/{request.user.username}/notifications')
