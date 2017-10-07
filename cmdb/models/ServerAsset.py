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
@File: ServerAsset.py
@Time: 9/26/17 10:29 AM
"""
from django.db import models
from .User import AssetUser
from .IDC import IDC


class ServerAsset(models.Model):
    STATUS_CHOICES = (
        ("In use", u"使用中"),
        ("Out of use", u"未使用"),
        ("fault", u"故障"),
        ("other", u"其他")
    )
    TYPE_CHOICES = (
        ("Server", u"物理机"),
        ("VM", u"虚拟机"),
        ("Docker", u"容器"),
        ("Storage", u"存储"),
    )
    create_by = models.CharField(verbose_name=u"创建者", max_length=32, blank=True)
    hostname = models.CharField(verbose_name=u"主机名", unique=True, max_length=50)
    port = models.IntegerField(verbose_name=u"远程连接端口", default=22)
    idc = models.ForeignKey(IDC, verbose_name=u"IDC", related_name="idc_assets")
    cabinet_no = models.CharField(verbose_name=u"机柜编号", max_length=30, null=True, blank=True)
    cabinet_pos = models.IntegerField(verbose_name=u"机柜位置", blank=True, null=True)
    certification = models.ForeignKey(AssetUser, verbose_name=u"远程登录凭证", related_name="cert_assets")
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="In use")
    type = models.CharField(choices=TYPE_CHOICES, max_length=10, default="Server")
    comment = models.CharField(verbose_name=u"备注", max_length=200, null=True, blank=True)

    # hardware
    product_serial = models.CharField(verbose_name=u"设备序列号", max_length=200, blank=True, null=True)
    product_uuid = models.CharField(verbose_name=u"设备UUID", max_length=50, blank=True, null=True)
    product_name = models.CharField(verbose_name=u"设备产商", max_length=50, blank=True, null=True)
    machine = models.CharField(verbose_name=u"架构", max_length=10, blank=True, null=True)

    # processor
    processor_type = models.CharField(verbose_name=u"CPU类型", max_length=80, blank=True, null=True)
    processor_count = models.IntegerField(verbose_name=u"CPU数量", default=1, blank=True, null=True)
    processor_core = models.IntegerField(verbose_name=u"CPU核心数", default=1, blank=True, null=True)

    # disks
    disks_total_capacity = models.CharField(verbose_name=u"磁盘总大小", max_length=10, blank=True, null=True)
    disks = models.CharField(verbose_name=u"磁盘信息", max_length=100, blank=True, null=True)

    # system
    node = models.CharField(verbose_name=u"节点名称", max_length=20, blank=True, null=True)
    bits = models.CharField(verbose_name=u"系统位数", max_length=5, blank=True, null=True)
    kernel = models.CharField(verbose_name=u"内核版本", max_length=15, blank=True, null=True)
    vendor = models.CharField(verbose_name=u"供应商", max_length=20, blank=True, null=True)
    swap_total = models.CharField(verbose_name=u"swap总和", max_length=20, blank=True, null=True)
    swap_free = models.CharField(verbose_name=u"swap剩余", max_length=20, blank=True, null=True)
    mem_total = models.CharField(verbose_name=u"内存", max_length=20, blank=True, null=True)
    mem_free = models.CharField(verbose_name=u"内存空闲", max_length=20, blank=True, null=True)
    os = models.CharField(verbose_name=u"系统类型", max_length=10, blank=True, null=True)
    distribution = models.CharField(verbose_name=u"发行版本", max_length=20, blank=True, null=True)

    # mounts
    mounts_num = models.IntegerField(verbose_name=u"分区数量", default=1)
    mounts = models.CharField(verbose_name=u"分区信息", max_length=200, blank=True, null=True)

    # network
    gateway = models.CharField(verbose_name=u"网关", max_length=50, blank=True, null=True)
    macaddr = models.CharField(verbose_name=u"网卡MAC地址", max_length=50, blank=True, null=True)
    ip = models.CharField(verbose_name=u"ipv4外网IP", max_length=50, null=True)
    networks = models.CharField(verbose_name=u"网络信息简介", max_length=400, blank=True, null=True)

    def __str__(self):
        return "<%s:%s>" % (self.hostname, self.product_serial)

    class Meta:
        ordering = ["hostname"]
        db_table = "cmdb_ServerAsset"
        verbose_name = u"服务器资产总表"
        verbose_name_plural = u"服务器资产总表"




