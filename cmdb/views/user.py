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
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, SingleObjectMixin, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from ..models import ServerAsset, AssetUser
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
    template_name = "cmdb/asset_user_create_update.html"
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


class AssetUserUpdateView(AdminUserRequiredMixin, UpdateView):
    model = AssetUser
    form_class = forms.AssetUserForm
    template_name = "cmdb/asset_user_create_update.html"

    def get_context_data(self, **kwargs):
        context = {
            "app": "资产管理",
            "action": "终端用户信息更新"
        }
        kwargs.update(context)
        return super(AssetUserUpdateView, self).get_context_data(**kwargs)

    def get_success_url(self):
        success_url = reverse_lazy("cmdb:asset-user-detail", kwargs={"pk": self.object.pk})
        return success_url


class AssetUserDetailView(AdminUserRequiredMixin, SingleObjectMixin, ListView):
    model = AssetUser
    template_name = "cmdb/asset_user_detail.html"
    context_object_name = "asset_user"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=AssetUser.objects.values("id", "username", "date_created", "create_by", "comment"))
        return super(AssetUserDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "app": u"资产管理",
            "action": u"终端用户详情"
        }
        kwargs.update(context)
        return super(AssetUserDetailView, self).get_context_data(**kwargs)


class AssetUserAssetView(AdminUserRequiredMixin, SingleObjectMixin, ListView):
    model = AssetUser
    template_name = "cmdb/asset_user_asset.html"
    context_object_name = "asset_user"

    def get(self, request, *args, **kwargs):
        # self.object = self.get_object(queryset=AssetUser.objects.values("id", "username", "cert_assets"))
        self.object = self.get_object(queryset=AssetUser.objects.all())
        return super(AssetUserAssetView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        assets_remain = ServerAsset.objects.exclude(id__in=self.object.cert_assets.all())
        context = {
            "app": u"资产管理",
            "action": u"终端用户资产详情",
            "assets_remain": assets_remain,
            "count": len(self.object.cert_assets.all())
        }
        kwargs.update(context)
        return super(AssetUserAssetView, self).get_context_data(**kwargs)

