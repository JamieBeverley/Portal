# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0017_auto_20170211_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='isStudy',
            field=models.BooleanField(default=False),
        ),
    ]
