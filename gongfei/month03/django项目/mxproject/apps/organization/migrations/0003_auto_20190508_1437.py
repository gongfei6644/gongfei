# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-08 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_teacher_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='desc',
            field=models.CharField(default='一个老师', max_length=200, verbose_name='描述'),
        ),
    ]
