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
@Time: 9/29/17 5:34 PM
"""
from django import forms

from ..models import IDC, AssetUser, ServerAsset


class IDCForm(forms.ModelForm):
    # assets = forms.ModelMultipleChoiceField(
    #     queryset=ServerAsset.objects.all(),
    #     label=u"资产",
    #     required=False,
    #     widget=forms.SelectMultiple(
    #         attrs={"class": "select2", "data-placeholder": u"选择资产"}
    #     )
    # )

    def __init__(self, *args, **kwargs):
        # if kwargs.get("instance"):
        #     initial = kwargs.get("initial", {})
        #     initial["assets"] = kwargs["instance"].assets.all()
        super(IDCForm, self).__init__(*args, **kwargs)

    def _save_m2m(self):
        super(IDCForm, self)._save_m2m()
        # assets = self.cleaned_data["assets"]
        # self.instance.assets.clear()
        # self.instance.assets.add(*tuple(assets))

    class Meta:
        model = IDC
        fields = ["name", "address", "tel", "contact", "contact_phone",
                  "intranet", "extranet", "operator", "bandwidth", "comment"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": u"IDC机房名称"}),
            "intranet": forms.TextInput(
                attrs={"placeholder": "IP段之间用逗号隔开，如：192.168.1.0/24，192.168.2.0/24"}
            ),
            "extranet": forms.TextInput(
                attrs={"placeholder": "IP段之间用逗号隔开，如：100.100.100.0/24，200.200.200.0/24"}
            ),
            "comment": forms.Textarea(
                attrs={"placeholder": "备注信息"}
            )
        }
        help_texts = {
            "name": "* 必须"
        }
