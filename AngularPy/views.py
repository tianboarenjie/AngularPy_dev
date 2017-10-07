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
@File: views.py
@Time: 9/25/17 8:35 PM
"""
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from users.models import User


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            pass
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # context = {}
        # kwargs.update(context)
        return super(IndexView, self).get_context_data(**kwargs)
