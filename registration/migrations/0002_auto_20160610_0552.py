# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-10 05:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visitors',
            old_name='secondName',
            new_name='lastName',
        ),
    ]
