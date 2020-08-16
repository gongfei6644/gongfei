# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      adminx.py
   Description :     
   Author :         gongyan
   Date：           2019/4/4
   Change Activity: 2019/4/4 14:49
-------------------------------------------------
"""
from .models import Teacher,CourseOrg,CityDict
import xadmin


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class TeacherAdmin(object):
    list_display = ['name', 'desc', 'work_years', 'work_company']
    search_fields = ['name', 'desc', 'work_years', 'work_company']
    list_filter = ['name', 'desc', 'work_years', 'work_company']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']
    # 设置搜索课程机构显示
    relfield_style = 'fk_ajax'


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)