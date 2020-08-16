from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from organization.models import CourseOrg,Teacher
from DjangoUeditor.models import UEditorField
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    teacher = models.ForeignKey(Teacher, verbose_name=u'机构讲师', blank=True,null=True)
    # detail = UEditorField(verbose_name=u'课程详情',width=600, height=300, imagePath="/course/ueditor/", filePath="/course/ueditor/",
    #          default='')
    degree = models.CharField(max_length=5, verbose_name=u'难度', choices=(('cj', u'初级'),('zj', u'中级'),('gj', u'高级')))
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    is_banner = models.BooleanField(default=False,verbose_name=u'是否轮播')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'封面图片')
    category = models.CharField(max_length=20, verbose_name=u'课程类别', default=u'后端开发')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    tag = models.CharField(default='', verbose_name=u'课程标签', max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    youneed_konw = models.CharField(default='', max_length=300, verbose_name=u'课程须知')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name=u'老师告诉你')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_num(self):
        """获取当前章节数"""
        return self.lesson_set.all().count()
    get_zj_num.short_description = u'章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://localhost:8000">跳转</a>')
    go_to.short_description = u'跳转'

    def get_learn_users(self):
        """展示学习过的用户"""
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取当前的章节信息
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
     class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        # 使用相同的数据，但不会生成新表
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        #获取章节视屏
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节名')
    name = models.CharField(max_length=100,verbose_name=u'视频名')
    url = models.CharField(max_length=200, verbose_name=u'视频地址', default="")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseSource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u'名称')
    download = models.FileField(upload_to='course/resouce/%Y/%m',verbose_name=u'文件资源',max_length=100)
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
