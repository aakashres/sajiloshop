# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-22 10:12
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0004_auto_20160822_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cart',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]
