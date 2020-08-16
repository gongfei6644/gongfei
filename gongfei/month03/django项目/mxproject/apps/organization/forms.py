# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      forms
   Description :     
   Author :         gongyan
   Date：           2019/5/8
   Change Activity: 2019/5/8 10:37
-------------------------------------------------
"""
from django import forms
from operations.models import UserAsk
import re

# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, max_length=5, min_length=5)


# 此处可以使用modelform来验证,代替了上面的form验证！
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法',code='mobile_invalidation')

