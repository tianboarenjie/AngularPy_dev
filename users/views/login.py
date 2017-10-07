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
@File: login.py
@Time: 9/25/17 8:42 PM
"""

from django.views.generic.edit import FormView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import reverse, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import authenticate
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from ..forms import UserLoginForm

__all__ = ["UserLoginView", "UserLogoutView"]


@method_decorator(sensitive_post_parameters(), name="dispatch")
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class UserLoginView(FormView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return redirect(self.get_success_url())
        return super(UserLoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=self.request.POST["username"], password=self.request.POST["password"])
        if user is not None:
            # print(user.username, user.password, dir(user._meta))
            # print(form.get_user())
            auth_login(self.request, user)
            return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, reverse("index"))
        )


@method_decorator(never_cache, name="dispatch")
class UserLogoutView(TemplateView):
    template_name = "_message.html"

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(UserLogoutView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "title": "用户注销成功",
            "messages": u"用户注销成功, 返回登录页面",
            "redirect_url": reverse("users:login"),
            "auto_redirect": True,
        }
        kwargs.update(context)
        return super(UserLogoutView, self).get_context_data(**kwargs)
