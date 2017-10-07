# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 18:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0005_auto_20171001_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverasset',
            name='certification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cert_assets', to='cmdb.AssetUser', verbose_name='远程登录凭证'),
        ),
        migrations.AlterField(
            model_name='serverasset',
            name='idc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='idc_assets', to='cmdb.IDC', verbose_name='IDC'),
        ),
    ]