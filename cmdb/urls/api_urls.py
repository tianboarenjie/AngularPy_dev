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
@File: api_urls.py
@Time: 9/29/17 7:45 PM
"""
from django.conf.urls import url
from rest_framework import routers
from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = "cmdb"

router = BulkRouter()
router.register(r"v1/idc", api.IDCViewSet, "idc")
router.register(r"v1/asset-user", api.AssetUserSet, "asset-user")
router.register(r"v1/asset", api.ServerAssetSet, "asset")

urlpatterns = [
    url(r"^v1/asset/(?P<pk>\d+)/refresh/$", api.ServerAssetRefreshView.as_view(), name="asset-refresh"),

    url(r"^v1/idc/(?P<pk>\d+)/asset/$", api.IDCUpdateAssetApi.as_view(), name="idc-update-asset"),

    url(r"^v1/asset-user/(?P<pk>\d+)/asset/$", api.AssetUserUpdateAssetApi.as_view(), name="asset-user-update-asset"),
]

urlpatterns += router.urls
