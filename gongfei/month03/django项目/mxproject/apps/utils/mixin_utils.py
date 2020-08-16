# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      mixin_utils
   Description :     
   Author :         gongyan
   Date：           2019/5/25
   Change Activity: 2019/5/25 22:10
-------------------------------------------------
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequireMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequireMixin,self).dispatch(request, *args, **kwargs)