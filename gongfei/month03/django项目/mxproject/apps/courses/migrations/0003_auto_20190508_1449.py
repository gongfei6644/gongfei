# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-08 14:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_course_org'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='learn_time',
            new_name='learn_times',
        ),
    ]
