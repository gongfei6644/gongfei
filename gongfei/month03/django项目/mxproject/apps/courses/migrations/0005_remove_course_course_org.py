# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-08 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20190508_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_org',
        ),
    ]
