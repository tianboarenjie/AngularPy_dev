# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0006_auto_20171002_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverasset',
            name='product_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='设备产商'),
        ),
    ]
