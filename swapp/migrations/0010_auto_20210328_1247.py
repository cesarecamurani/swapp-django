# Generated by Django 3.1.7 on 2021-03-28 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swapp', '0009_auto_20210327_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='swapprequest',
            name='offered_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offered_product_id', to='swapp.item'),
        ),
        migrations.AlterField(
            model_name='swapprequest',
            name='requested_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='requested_product_id', to='swapp.item'),
        ),
    ]