# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-07-03 09:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctitle', models.CharField(max_length=50, null=True, verbose_name='汽车名称')),
                ('engineNo', models.CharField(max_length=50, null=True, verbose_name='发动机号')),
                ('regist_date', models.DateField(verbose_name='上牌日期')),
                ('mileage', models.IntegerField(verbose_name='公里数')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='价格')),
                ('debt', models.BooleanField(default=False, verbose_name='债务')),
                ('picture', models.ImageField(default='normal.png', upload_to='img/cars', verbose_name='图片')),
                ('promise', models.TextField(verbose_name='卖家承诺')),
                ('isPurchase', models.BooleanField(default=False, verbose_name='是否购买')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('examine', models.IntegerField(choices=[(0, '审核中'), (1, '审核通过'), (2, '审核不通过')], default=0, verbose_name='审核进度')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.Brand')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '车辆表',
                'verbose_name_plural': '车辆表',
            },
        ),
    ]
