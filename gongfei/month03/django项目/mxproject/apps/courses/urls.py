# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      urls.py
   Description :    这是课程中的路由选择
   Author :         gongyan
   Date：           2019/5/16
   Change Activity: 2019/5/16 20:02
-------------------------------------------------
"""

from django.conf.urls import url,include
from .views import *

urlpatterns = [
    # 课程相关的url 配置
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # 课程内容页
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    # 课程评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    # 访问视频地址
    url(r'^video(?P<video_id>\d+)/$', VideoPlayView.as_view(),name='video_play')
]