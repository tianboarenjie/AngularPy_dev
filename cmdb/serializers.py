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
@File: serializers.py
@Time: 9/29/17 7:26 PM
"""

from rest_framework import viewsets, serializers, generics
from rest_framework_bulk import BulkSerializerMixin
# import makedown2

from .models import IDC, ServerAsset, AssetUser

import json

#
# class


class AssetUserSerializer(serializers.ModelSerializer):
    assets_amount = serializers.SerializerMethodField()
    assets_list = serializers.SerializerMethodField()
    cert_assets = serializers.PrimaryKeyRelatedField(many=True, queryset=ServerAsset.objects.values("hostname"))

    class Meta:
        model = AssetUser
        fields = ["id", "username", "comment", "cert_assets", "assets_amount", "assets_list"]

    @staticmethod
    def get_assets_amount(obj):
        return obj.cert_assets.count()

    @staticmethod
    def get_assets_list(obj):
        if obj.cert_assets.count() is 0:
            return json.dumps(obj.cert_assets.name)
        else:
            tmp = obj.cert_assets.get_queryset().values("hostname")
            result = " "
            for host in tmp:
                result += host["hostname"]
            return result

    def get_field_names(self, declared_fields, info):
        fields = super(AssetUserSerializer, self).get_field_names(declared_fields, info)
        fields.append("assets_amount")
        fields.append("assets_list")
        return fields


class IDCSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    assets_amount = serializers.SerializerMethodField()
    idc_assets = serializers.PrimaryKeyRelatedField(many=True, queryset=ServerAsset.objects.all())

    class Meta:
        model = IDC
        fields = "__all__"

    @staticmethod
    def get_assets_amount(obj):
        return obj.idc_assets.count()

    def get_field_names(self, declared_fields, info):
        fields = super(IDCSerializer, self).get_field_names(declared_fields, info)
        fields.append("assets_amount")
        return fields


class IDCUpdateAssetSerializer(serializers.ModelSerializer):
    idc_assets = serializers.PrimaryKeyRelatedField(many=True, queryset=ServerAsset.objects.all())

    class Meta:
        model = IDC
        fields = ["id", "idc_assets"]


class ServerAssetSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    idc = serializers.CharField()
    certification = serializers.CharField()
    # certification_name = serializers.SerializerMethodField()
    # cert_assets = serializers.PrimaryKeyRelatedField(many=True, queryset=AssetUser.objects.values("username"))

    class Meta:
        model = ServerAsset
        # fields = ["id", "hostname", "idc", "type", "ip", "port", "status", "certification"]
        fields = "__all__"
    # @staticmethod
    # def get_idc_name(obj):
    #     return obj.idc.get_queryset().values("name")
    #
    # @staticmethod
    # def get_certification_name(obj):
    #     return obj.certification.get_queryset().values("username")
    #
    # def get_field_names(self, declared_fields, info):
    #     fields = super(ServerAssetSerializer, self).get_field_names(declared_fields, info)
    #     fields.append("idc_name")
    #     fields.append("certification_name")
    #     return fields
