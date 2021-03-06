# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 01:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DC', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow_records',
            name='user_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='cost',
            name='consume_address',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cost',
            name='consume_type',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='cost',
            name='user_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='job',
            name='user_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='messages',
            name='user_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='schoolarship',
            name='user_id',
            field=models.CharField(max_length=30),
        ),
    ]
