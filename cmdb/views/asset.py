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
@File: asset.py
@Time: 9/27/17 8:11 PM
"""
from users.utils import *
from ..models import ServerAsset
from .. import forms

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from django.urls import reverse_lazy

import json


class ServerAssetListView(AdminUserRequiredMixin, TemplateView):
    template_name = "cmdb/asset_list.html"

    def get_context_data(self, **kwargs):
        context = {
            "app": "资产管理",
            "action": "资产信息",
        }
        kwargs.update(context)
        return super(ServerAssetListView, self).get_context_data(**kwargs)


class ServerAssetCreateView(AdminUserRequiredMixin, CreateView):
    model = ServerAsset
    form_class = forms.ServerAssetCreateForm
    template_name = "cmdb/asset_create_update.html"
    success_url = reverse_lazy("cmdb:asset-list")

    def form_valid(self, form):
        self.asset = asset = form.save()
        asset.create_by = self.request.user.username or "Admin"
        asset.save()
        return super(ServerAssetCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = {
            "app": "资产管理",
            "action": "创建资产",
        }
        kwargs.update(context)
        return super(ServerAssetCreateView, self).get_context_data(**kwargs)


class ServerAssetUpdateView(AdminUserRequiredMixin, UpdateView):
    model = ServerAsset
    form_class = forms.ServerAssetUpdateForm
    template_name = "cmdb/asset_create_update.html"

    def get_context_data(self, **kwargs):
        context = {
            "app": "资产管理",
            "action": "资产信息更新",
        }
        kwargs.update(context)
        return super(ServerAssetUpdateView, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super(ServerAssetUpdateView, self).form_invalid(form)

    def get_success_url(self):
        success_url = reverse_lazy("cmdb:asset-detail", kwargs={"pk": self.object.pk})
        return success_url


class ServerAssetDetailView(DeleteView):
    model = ServerAsset
    context_object_name = "asset"
    template_name = "cmdb/asset_detail.html"

    def get_context_data(self, **kwargs):
        networks = self.get_networks(),
        disks = self.get_disks(),
        mounts = self.get_mounts(),
        context = {
            "app": "资产信息",
            "action": "资产状态详情",
            "networks": networks,
            "disks": disks,
            "mounts": mounts,
        }
        kwargs.update(context)
        return super(ServerAssetDetailView, self).get_context_data(**kwargs)

    def get_networks(self):
        if self.object.networks is None:
            return "None"
        return json.loads(self.object.networks)

    def get_disks(self):
        if self.object.disks is None:
            return "None"
        return json.loads(self.object.disks)

    def get_mounts(self):
        if self.object.mounts is None:
            return "None"
        return json.loads(self.object.mounts)
