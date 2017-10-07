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
@File: tasks.py
@Time: 10/7/17 10:03 AM
"""
from celery import shared_task
import json

from django.core.cache import cache

from .ansible.hostinfo import HostsInfo
from .utils import get_object_or_none
from .models import ServerAsset


@shared_task
def refresh_asset_hardware_info(assets):
    result = HostsInfo(assets).gather_cmdb_info()
    for hostname, info in result["contacted"].items():
        asset = get_object_or_none(ServerAsset, hostname=hostname)
        if not asset:
            continue
        for k, v in info.items():
            setattr(asset, k, json.dumps(v))
        asset.save()
    return result["dark"]
