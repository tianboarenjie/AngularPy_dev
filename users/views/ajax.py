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
@File: ajax.py
@Time: 9/25/17 8:42 PM
"""
import json
from captcha.models import CaptchaStore
from captcha.views import captcha_image_url
from django.http import JsonResponse, HttpResponse


def check(request):
    if request.is_ajax():
        captcha_obj = CaptchaStore.objects.filter(response=request.GET["response"],
                                                  hashkey=request.GET["hashkey"])
        if captcha_obj:
            result = {"status": 1}
        else:
            result = {"status": 0}
        return JsonResponse(result)
    else:
        result = {"status": 0}
        return JsonResponse(result)


def refresh(request):
    if not request.is_ajax():
        pass

    new_key = CaptchaStore.generate_key()
    to_json_response = {
        "key": new_key,
        "image_url": captcha_image_url(new_key),
    }

    print(CaptchaStore.objects.all())
    CaptchaStore.save(**to_json_response)
    return HttpResponse(json.dumps(to_json_response), content_type="application/json")

