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
@Time: 9/25/17 8:49 PM
"""
from django.conf.urls import url

from .. import views

app_name = "users"

urlpatterns = [
    # login view
    url(r"login$", views.UserLoginView.as_view(), name="login"),
    url(r"logout$", views.UserLogoutView.as_view(), name="logout"),
    url(r"captcha_check$", views.check, name="captcha_check"),
    # url(r"captcha_refresh$", views.refresh, name="captcha_refresh")

    url(r"user/$", views.UserListView.as_view(), name="system-user-list")
]
