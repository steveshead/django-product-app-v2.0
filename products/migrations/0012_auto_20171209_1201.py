# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-09 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20171209_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('Choose', 'Choose'), ('T-Shirt', 'T-Shirt'), ('PSD Template', 'PSD Template'), ('HTML', 'HTML'), ('Python', 'Python'), ('Other', 'Other')], default='choose', max_length=15),
        ),
    ]
