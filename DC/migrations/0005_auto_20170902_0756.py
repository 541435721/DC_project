# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 23:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DC', '0004_auto_20170901_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='shopping_time',
            field=models.DateTimeField(),
        ),
    ]
