# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-13 10:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projman', '0005_projcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='private',
        ),
    ]
