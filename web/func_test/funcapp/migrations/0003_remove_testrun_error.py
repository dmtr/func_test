# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 16:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funcapp', '0002_auto_20160725_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testrun',
            name='error',
        ),
    ]
