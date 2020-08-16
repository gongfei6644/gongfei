# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      urls
   Description :     
   Author :         gongyan
   Date：           2019/5/29
   Change Activity: 2019/5/29 0:03
-------------------------------------------------
"""
from django.conf.urls import url, include
from .views import *

urlpatterns =[
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像上床
    url(r'image/upload/$', UpLoadImageView.as_view(), name='user_image'),
    # 用户修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 用于发送邮箱验证码
    url(r'sendemail/$', SendEmailVerifyView.as_view(), name='sendmail_code'),
    # 修改邮箱
    url(r'update_email/$', UpdateEmailView.as_view(), name='update_email'),
    # 我的课程页面
    url(r'^mycourse/$', MyCourseView.as_view(),name='mycourse'),
    # 我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfavorg'),
    # 访问我收藏的授课教师
    url(r'myfav/teacher/$',MyFavTeacherView.as_view(),name='myfavteacher'),
    # 我收藏的课程
    url(r'myfav/course/$',MyFavCourseView.as_view(), name='myfavcourse'),
    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),

]