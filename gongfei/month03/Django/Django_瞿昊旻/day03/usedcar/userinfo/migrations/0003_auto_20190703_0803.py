# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-07-03 08:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0002_bankcard'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name': '用户列表', 'verbose_name_plural': '用户列表展示'},
        ),
    ]
