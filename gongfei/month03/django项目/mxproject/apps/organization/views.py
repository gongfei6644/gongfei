# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from django.http import HttpResponse
from django.db.models import Q
from courses.models import Course
from operations.models import UserFavorite
import json

# Create your views here.


class OrgView(View):
    def get(self, request):
        # 返回课程机构的首页
        all_org = CourseOrg.objects.all()
        # 找出最热门的授课机构
        hot_orgs = all_org.order_by('-click_nums')[:4]
        all_cities = CityDict.objects.all()
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_org = all_org.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords))
        # 取出筛选城市
        city_id = request.GET.get('city', '')
        # 取出筛选城市
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))
        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_org = all_org.filter(category=category)
        org_nums = all_org.count()
        # 对课程数进行排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_org = all_org.order_by('-students')
            elif sort == 'courses':
                all_org = all_org.order_by('-course_num')
        # 对课程机构进行分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_org, 4, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort
        })


class AddUserAskView(View):
    """
    用户添加咨询的表单的提交
    """
    def post(self,request):
        ask_form = UserAskForm(request.POST)
        if ask_form.is_valid():
            user_ask = ask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type = 'application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 课程机构点击事件操作
        course_org.click_nums += 1
        course_org.save()
        # 取出所有的课程,有外键的都可以用
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html',{
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page
        })


class OrgCourseView(View):
    """
    机构课程页
    """
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 取出所有的课程,有外键的都可以用
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page
        })


class OrgDescView(View):
    """
    机构介绍页面
    """
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 取出所有的课程,有外键的都可以用
        return render(request, 'org-detail-desc.html',{
            'course_org': course_org,
            'current_page': current_page
        })


class OrgTeacherView(View):
    """
    机构讲师详情页面
    """
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html',{
            'all_courses': all_teachers,
            'course_org': course_org,
            'current_page': current_page
        })


class AddFavView(View):
    """
    用户收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            print(request.user.is_authenticated())
            # 判断用户登录状态
            return HttpResponse(json.dumps({'status': 'fail','msg': '用户未登录'}),
                                content_type='application/json')
        exist_record = UserFavorite.objects.filter(
            user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            # 如果记录已经存在，表示用户取消收藏
            exist_record.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '收藏'}),
                                content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) >0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                # 如果收藏成功之后，则会去对操作数加1
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse(json.dumps({'status': 'success', 'msg':'已收藏'}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏出错'}),
                                    content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self,request):
        all_teacher = Teacher.objects.all()
        # 讲师搜索
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_teacher = all_teacher.filter(Q(name__icontains=search_keywords))
        # 热门排序讲师排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teacher = all_teacher.order_by('-click_nums')

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:4]
        # 对讲师进行分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher, 5, request=request)
        teachers = p.page(page)
        return render(request, 'teachers-list.html', {
            'all_teacher': teachers,
            'sorted_teacher': sorted_teacher,
            'sort': sort
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_course = Course.objects.filter(teacher=teacher)
        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3,fav_id=teacher.id):
            has_teacher_faved = True
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org.id):
            has_org_faved = True


        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_course': all_course,
            'sorted_teacher': sorted_teacher,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved
        })


