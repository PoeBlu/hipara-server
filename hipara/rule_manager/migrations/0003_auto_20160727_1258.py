# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-27 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rule_manager', '0002_auto_20151202_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadata',
            name='value',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
