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


class ServerAssetCreateForm(forms.ModelForm):
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
            "comment": forms.Textarea(
                attrs={"placeholder": "备注信息"}
            )

        }
        help_texts = {
            "hostname": "* 必须",
            "type": "* 必须",
            "idc": "* 必须，IDC应该在系统内存在！",
            "certification": "* 必须，终端凭证应该在系统内存在！",
            "ip": "* 必须",
            "status": "* 必须",
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


class ServerAssetUpdateForm(forms.ModelForm):
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
            "comment": forms.Textarea(
                attrs={"placeholder": "备注信息"}
            )

        }
        help_texts = {
            "hostname": "* 必须",
            "type": "* 必须",
            "idc": "* 必须，IDC应该在系统内存在！",
            "certification": "* 必须，终端凭证应该在系统内存在！",
            "ip": "* 必须",
            "status": "* 必须",
        }
