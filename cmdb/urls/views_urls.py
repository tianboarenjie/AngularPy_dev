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
@File: views_urls.py
@Time: 9/27/17 8:09 PM
"""
from django.conf.urls import url
from .. import views

app_name = "cmdb"

urlpatterns = [
    # asset
    url(r"^$", views.AssetListView.as_view(), name="asset-index"),
    url(r"^asset/$", views.AssetListView.as_view(), name="asset-list"),
    url(r"^asset/create/$", views.AssetCreateView.as_view(), name="asset-create"),
    url(r"^asset/(?P<pk>[0-9]+)/$", views.AssetDetailView.as_view(), name="asset-detail"),

    # idc
    url(r"^idc/$", views.IDCListView.as_view(), name="idc-list"),
    url(r"^idc/create/$", views.IDCCreateView.as_view(), name="idc-create"),
    url(r"^idc/(?P<pk>\d+)/$", views.IDCDetailView.as_view(), name="idc-detail"),
    url(r"^idc/(?P<pk>\d+)/asset/$", views.IDCAssetView.as_view(), name="idc-asset"),

    # user
    url(r"^user/$", views.AssetUserListView.as_view(), name="asset-user-list"),
    url(r"^user/create/$", views.AssetUserCreateView.as_view(), name="asset-user-create"),
    url(r"^user/(?P<pk>\d+)/$", views.AssetUserDetailView.as_view(), name="asset-user-detail"),
    url(r"^user/(?P<pk>\d+)/asset/$", views.AssetUserAssetView.as_view(), name="asset-user-asset"),

]
