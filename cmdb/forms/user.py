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
@Time: 9/29/17 10:05 PM
"""
from django import forms

from ..models import AssetUser


class AssetUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, max_length=100,
        strip=True, required=True,
    )

    class Meta:
        model = AssetUser
        fields = ["username", "password", "comment"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": u"终端用户名"}),
            "comment": forms.Textarea(attrs={"placeholder": u"备注"}),
        }
        help_texts = {
            "username": "* 必须",
        }
