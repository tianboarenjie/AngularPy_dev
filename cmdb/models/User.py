#!/usr/bin/env python3.5
# -*- encoding: utf-8  -*-
"""
@Version: 1.0
@Author: tianbaorenjie
@License: 
@Contact: tianbaorenjie@163.com
@Site: http://
@Software: PyCharm
@Project: AngularPy_dev
@File: User.py
@Time: 9/26/17 10:41 AM
"""
from django.db import models
import time


class AssetUser(models.Model):
    username = models.CharField(verbose_name=u"远程用户名", max_length=30, null=True)
    password = models.CharField(verbose_name=u"远程用户密码", max_length=30, null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    create_by = models.CharField(verbose_name=u"创建者", max_length=32, blank=True)
    comment = models.CharField(verbose_name=u"备注", max_length=200, blank=True, null=True)

    def __str__(self):
        return "%s(%s)" % (self.username, self.date_created.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        ordering = ["username", "date_created"]
        db_table = "cmdb_AssetUser"
        verbose_name = u"资产用户总表"
        verbose_name_plural = u"资产用户总表"
