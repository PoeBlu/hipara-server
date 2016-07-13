# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-16 08:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('alert_id', models.AutoField(primary_key=True, serialize=False)),
                ('hostName', models.CharField(max_length=128)),
                ('fileName', models.CharField(max_length=200)),
                ('alertMessage', models.CharField(max_length=250)),
                ('timeStamp', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_alert', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]