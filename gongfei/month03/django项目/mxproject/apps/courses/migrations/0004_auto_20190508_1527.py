# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-08 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20190508_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='学习时长(分钟数)'),
        ),
        migrations.AddField(
            model_name='video',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='学习时长(分钟数)'),
        ),
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('cj', '初级'), ('zj', '中级'), ('gj', '高级')], max_length=5, verbose_name='难度'),
        ),
    ]
