# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-19 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
