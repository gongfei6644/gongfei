# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      adminx.py
   Description :     
   Author :         gongyan
   Date：           2019/4/4
   Change Activity: 2019/4/4 11:19
-------------------------------------------------
"""
import xadmin
from .models import Course,Lesson,CourseSource,Video,BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseSource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students','get_zj_num','go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    # 可以设置某些字段的默认排序方式
    ordering = ['-click_num']
    # 可以设置某些字段的属性：只读，后台不能修改
    readonly_fields = ['fav_nums']
    # 列表页可以直接在后台中进行编辑课程的内容
    list_editable = ['degree', 'desc']
    # 设置不显示的字段
    exclude = ['click_num']
    inlines = [LessonInline,CourseResourceInline]

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    # 可以设置某些字段的默认排序方式
    ordering = ['-click_num']
    # 可以设置某些字段的属性：只读，后台不能修改
    readonly_fields = ['fav_nums']
    # 设置不显示的字段
    exclude = ['click_num']
    inlines = [LessonInline,CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner=True)
        return qs



class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseSourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseSource, CourseSourceAdmin)







