from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
import json

from .models import Course,CourseSource,Video
from operations.models import UserFavorite,CourseComment,UserCourse
from utils.mixin_utils import LoginRequireMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_num')[:3]

        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|
                                             Q(desc__icontains=search_keywords)|
                                             Q(detail__icontains=search_keywords))

        # 课程的排序功能
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_num')
        # 对课程内容进行分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        course = p.page(page)
        return render(request, 'course-list.html', {
            'all_course': course,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_num += 1
        course.save()

        # 课程收藏的功能
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course.id,
                                           fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user,
                                            fav_id=course.course_org.id,
                                            fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            related_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'related_course': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequireMixin, View):
    """
    课程章节信息页面
    此处的逻辑比较复杂，注意理解
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_courser.course.id for user_courser in user_courses]
        # 获取学过该用户学过的其他所有课程
        related_course = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        all_resource = CourseSource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_course': all_resource,
            'related_course': related_course
            })


class CourseCommentView(LoginRequireMixin, View):
    """课程评论处理模块"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resource = CourseSource.objects.filter(course=course)
        all_comment = CourseComment.objects.all()
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resource': all_resource,
            'all_comments': all_comment
        })


class AddCommentView(View):
    """
    用户添加评论功能
    """
    def post(self,request):
        # 先判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse(
                "{'status':'fail','msg':'用户未登录'}",
                content_type="application/json"
            )
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(
                "{'status':'success','msg':'添加成功'}",
                content_type="application/json"
            )
        else:
            return HttpResponse(
                "{'status':'fail','msg':'添加失败'}",
                content_type="application/json"
            )

class VideoPlayView(View):
    """
    视频播放
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()
        # 查询用户是否关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_courser.course.id for user_courser in user_courses]
        # 获取学过该用户学过的其他所有课程
        related_course = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        all_resource = CourseSource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_course': all_resource,
            'related_course': related_course,
            'video': video
            })
