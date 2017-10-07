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
@Time: 9/28/17 1:49 AM
"""

from django.views.generic import TemplateView

from users.utils import AdminUserRequiredMixin


class UserListView(AdminUserRequiredMixin, TemplateView):
    template_name = "users/user_list.html"

    def get_context_data(self, **kwargs):
        context = {
            "app": "用户",
            "action": "用户列表",
        }
        kwargs.update(context)
        return super(UserListView, self).get_context_data(**kwargs)
