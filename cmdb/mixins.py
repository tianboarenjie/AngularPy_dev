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
@File: mixins.py
@Time: 9/29/17 8:12 PM
"""
from django.db import models


class IDInfilterMixin(object):
    def filter_aueeryset(self, queryset):
        id_list = self.request.query_params.get("id__in")
        if id_list:
            import json
            try:
                ids = json.loads(id_list)
            except Exception as e:
                return queryset
            if isinstance(ids, list):
                queryset = queryset.filter(id_list=ids)
        return queryset
