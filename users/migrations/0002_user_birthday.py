# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Birth day'),
        ),
    ]
