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
@File: IDC.py
@Time: 9/26/17 10:17 AM
"""

from django.db import models


class IDC(models.Model):
    name = models.CharField(verbose_name=u"机房名称", max_length=30, null=True, blank=True)
    address = models.CharField(verbose_name=u"机房地址", max_length=100, null=True, blank=True)
    tel = models.CharField(verbose_name=u"机房电话", max_length=30, null=True, blank=True)
    contact = models.CharField(verbose_name=u"机房联系人", max_length=30, null=True, blank=True)
    contact_phone = models.CharField(verbose_name=u"联系人电话", max_length=30, null=True, blank=True)
    intranet = models.CharField(verbose_name=u"内网IP范围", max_length=50, blank=True, null=True)
    extranet = models.CharField(verbose_name=u"外网IP范围", max_length=50, blank=True, null=True)
    operator = models.CharField(verbose_name=u"维护商", max_length=32, blank=True)
    bandwidth = models.CharField(verbose_name=u"接入带宽", max_length=30, null=True, blank=True)
    create_by = models.CharField(verbose_name=u"创建者", max_length=32, blank=True)
    comment = models.CharField(verbose_name=u"备注", max_length=200, null=True, blank=True)

    def __str__(self):
        return "%s(%s)" % (self.name, self.extranet)

    class Meta:
        ordering = ["name"]
        db_table = "cmdb_IDC"
        verbose_name = u"IDC总表"
        verbose_name_plural = u"IDC总表"
