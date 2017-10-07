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
@Time: 10/1/17 11:14 PM
"""
from django import forms

from ..models import ServerAsset


class AssetCreateForm(forms.ModelForm):
    class Meta:
        model = ServerAsset
        fields = [
            "hostname", "type", "idc", "ip", "port", "certification",
            "status", "cabinet_no", "cabinet_pos", "comment",
        ]
        widgets = {
            "type": forms.Select(
                attrs={"class": "select2",
                       "data-placeholder": u"选择设备类型"}
            ),
            "idc": forms.Select(
                attrs={"class": "select2",
                       "data-placeholder": u"IDC机房"}
            ),
            "certification": forms.Select(
                attrs={"class": "select2",
                       "data-placeholder": u"登录凭证"}
            ),

        }
        help_texts = {
            "hostname": "* required",
            "type": "* required",
            "idc": "* required",
            "certification": "* required",
            "ip": "* required",
            "status": "* required",
        }

    def clean_type(self):
        if not self.cleaned_data["type"]:
            raise forms.ValidationError(u"必须选择资产类型")
        return self.cleaned_data["type"]

    def clean_certification(self):
        if not self.cleaned_data["certification"]:
            raise forms.ValidationError(u"必须指定登录用户凭证")
        return self.cleaned_data["certification"]

    def clean_idc(self):
        if not self.cleaned_data["idc"]:
            raise forms.ValidationError(u"必须指定IDC机房")
        return self.cleaned_data["idc"]
