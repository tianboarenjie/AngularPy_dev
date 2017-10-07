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
@File: idc.py
@Time: 9/28/17 11:48 PM
"""

from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView

from users.utils import AdminUserRequiredMixin

from ..forms import IDCForm
from ..models import IDC


class IDCListView(AdminUserRequiredMixin, TemplateView):
    template_name = "cmdb/idc_list.html"

    def get_context_data(self, **kwargs):
        context = {
            "app": "资产管理",
            "action": "IDC列表",
        }
        kwargs.update(context)
        return super(IDCListView, self).get_context_data(**kwargs)


class IDCCreateView(AdminUserRequiredMixin, CreateView):
    module = IDC
    form_class = IDCForm
    template_name = "cmdb/idc_create_update.html"
    success_url = reverse_lazy("cmdb:idc-list")

    def get_context_data(self, **kwargs):
        context = {
            "app": u"资产管理",
            "action": u"创建IDC"
        }
        kwargs.update(context)
        return super(IDCCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        idc = form.save(commit=False)
        idc.create_by = self.request.user.username or "System"
        idc.save()
        return super(IDCCreateView, self).form_valid(form)
