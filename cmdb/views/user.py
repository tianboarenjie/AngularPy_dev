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
@File: user.py
@Time: 9/27/17 11:19 PM
"""
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from ..models.User import AssetUser
from .. import forms
from users.utils import AdminUserRequiredMixin


class AssetUserListView(AdminUserRequiredMixin, TemplateView):
    template_name = "cmdb/asset_user_list.html"

    def get_context_data(self, **kwargs):
        context = {
            "app": "资产信息",
            "action": "终端用户信息",
        }
        kwargs.update(context)
        return super(AssetUserListView, self).get_context_data(**kwargs)


class AssetUserCreateView(AdminUserRequiredMixin, CreateView):
    model = AssetUser
    form_class = forms.AssetUserForm
    template_name = "cmdb/asset_user_create.html"
    success_url = reverse_lazy("cmdb:asset-user-list")

    def get_context_data(self, **kwargs):
        context = {
            "app": u"资产管理",
            "action": u"创建终端用户"
        }
        kwargs.update(context)
        return super(AssetUserCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        assetuser = form.save(commit=False)
        assetuser.create_by = self.request.user.username or "System"
        assetuser.save()
        return super(AssetUserCreateView, self).form_valid(form)

