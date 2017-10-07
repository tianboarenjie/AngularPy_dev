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
@File: api.py
@Time: 9/29/17 8:05 PM
"""
from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import BulkModelViewSet, BulkDestroyAPIView
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from django_filters.rest_framework import DjangoFilterBackend

from .utils import get_object_or_none
from .mixins import IDInfilterMixin
from . import serializers
from .tasks import refresh_asset_hardware_info
from .models import IDC, ServerAsset, AssetUser
from users.permissions import IsSuperUser


class IDCViewSet(IDInfilterMixin, BulkModelViewSet):
    queryset = IDC.objects.all()
    serializer_class = serializers.IDCSerializer
    permission_classes = (IsSuperUser,)


class AssetUserSet(IDInfilterMixin, BulkModelViewSet):
    queryset = AssetUser.objects.all()
    serializer_class = serializers.AssetUserSerializer
    permission_classes = (IsSuperUser,)


class ServerAssetSet(IDInfilterMixin, BulkModelViewSet):
    queryset = ServerAsset.objects.all()
    serializer_class = serializers.ServerAssetSerializer
    permission_classes = (IsSuperUser,)


class ServerAssetRefreshView(generics.RetrieveAPIView):
    queryset = ServerAsset.objects.all()
    serializer_class = serializers.ServerAssetSerializer
    permission_classes = (IsSuperUser,)

    def retrieve(self, request, *args, **kwargs):
        asset_id = kwargs.get("pk")
        temp = get_object_or_none(ServerAsset, pk=asset_id)
        asset = {
            "hostname": temp.hostname,
            "ip": temp.ip,
            "port": temp.port or 22,
            "username": temp.certification.username,
            "password": temp.certification.password,
        }
        print([asset])
        result = refresh_asset_hardware_info([asset])
        if len(result) == 0:
            return super(ServerAssetRefreshView, self).retrieve(result, *args, **kwargs)
        else:
            return Response(result, status=505)
