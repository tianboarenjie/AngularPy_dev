# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0007_serverasset_product_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serverasset',
            old_name='ipv4_extranet',
            new_name='ip',
        ),
        migrations.RemoveField(
            model_name='serverasset',
            name='ipv4_intranet',
        ),
        migrations.RemoveField(
            model_name='serverasset',
            name='ipv6_extranet',
        ),
        migrations.RemoveField(
            model_name='serverasset',
            name='ipv6_intranet',
        ),
        migrations.AddField(
            model_name='serverasset',
            name='networks',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='网络信息简介'),
        ),
    ]
