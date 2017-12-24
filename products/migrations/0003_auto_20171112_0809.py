# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('tshirt', 'T-Shirt'), ('sweater', 'Sweater'), ('poster', 'Poster'), ('painting', 'Painting'), ('other', 'Other')], default='tshirt', max_length=6),
        ),
    ]