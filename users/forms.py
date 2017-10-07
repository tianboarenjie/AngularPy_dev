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
@File: forms.py
@Time: 9/25/17 8:41 PM
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, authenticate
from captcha.fields import CaptchaField


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=u"用户名", max_length=100)
    password = forms.CharField(
        label=u"密码", widget=forms.PasswordInput, max_length=100, strip=False
    )
    captcha = CaptchaField()

    def clean(self):
        try:
            self.cleaned_data["captcha"]
        except Exception as err:
            pass
            # print(err)
            raise forms.ValidationError(u"验证码错误，请重新输入！")
        # print(self.cleaned_data)
        user = authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password"])
        if user is None:
            raise forms.ValidationError(u"用户名或密码错误，请确认后重新登录！")
