# Generated by Django 3.1.7 on 2021-03-26 13:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swapp', '0007_swapprequest_trace_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='swapprequest',
            name='closed_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
