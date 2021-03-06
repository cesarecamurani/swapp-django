# Generated by Django 3.1.7 on 2021-03-17 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donations',
            old_name='donor_id',
            new_name='donor',
        ),
        migrations.RenameField(
            model_name='donations',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='owner_id',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='swapprequest',
            old_name='offered_product_id',
            new_name='offered_product',
        ),
        migrations.RenameField(
            model_name='swapprequest',
            old_name='requested_product_id',
            new_name='requested_product',
        ),
    ]
