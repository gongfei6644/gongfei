# -*- coding:utf-8 -*-
import json
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

from pure_pagination import Paginator,EmptyPage,PageNotAnInteger


from .models import UserProfile,EmailVerifyRecord,Banner
from .forms import *
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequireMixin
from operations.models import UserCourse, UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from courses.models import Course
# Create your views here.


# 继承modelBackend
class CustomBackend(ModelBackend):
    # 自带的认证用户名方法
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        reg_form = RegisterForm()
        return render(request, 'register.html', {'reg_form':reg_form})

    def post(self,request):
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                    return render(request, 'register.html', {'reg_form': reg_form, 'msg': '用户已经存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册达内教育'
            user_message.save()

            send_register_email(user_name,'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'resg_form': reg_form})


class LogoutView(View):
    def get(self,request):
        logout(request)
        # 退出登录 重定向
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})

    def post(self,request):
        login_from = LoginForm(request.POST)
        if login_from.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'index.html',{'msg': '请激活账户'})
            else:
                return render(request,'login.html',{'msg': '用户名或者密码错误！'})
        else:
            return render(request, 'login.html',{'login_form':login_from.errors})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active.html')
        return render(request,'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request,'send_success.html')


class ResetUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html',{'email': email})
        else:
            return render(request, 'active.html')
        return render(request,'login.html')


class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            print(request.POST)
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html', {
                    'msg': '两次输入的密码不一致！',
                    'email': email
                })
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {
                'msg': '请输入密码！',
                'email': email
            })


class UserInfoView(LoginRequireMixin,View):
    """
    用户个人信息处理函数
    """
    def get(self,request):
        return render(request, 'usercenter-info.html', {})

    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}',
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors),
                                content_type='application/json')




class UpLoadImageView(LoginRequireMixin, View):
    """
    用户头像上传处理视图
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST,
                                     request.FILES,
                                     instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse('{"status":"success"}',
                                content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}',
                                content_type='application/json')

class UpdatePwdView(View):
    """
    用户在主页修改密码
    """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',
                                     content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}',
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors),
                                content_type='application/json')


class SendEmailVerifyView(LoginRequireMixin,View):
    """
    用来发送邮箱验证码
    """
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}',
                                content_type='application/json')
        send_register_email(email,'update_email',)
        return HttpResponse('{"status":"success"}',
                                content_type='application/json')


class UpdateEmailView(LoginRequireMixin, View):
    """
    用来修改邮箱视图
    """
    def post(self,request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_record = EmailVerifyRecord.objects.filter(email=email,
                                                          code=code,
                                                          send_type='update_email')
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}',
                                content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}',
                                content_type='application/json')


class MyCourseView(LoginRequireMixin,View):
    """
    用户个人课程页面
    """
    def get(self,request):
        user_courses= UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_courses': user_courses
        })


class MyFavOrgView(LoginRequireMixin,View):
    """
    我收藏的org
    """
    def get(self,request):
        orglist = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            orglist.append(org)
        return render(request,'usercenter-fav-org.html',{
            'orglist':orglist
        })


class MyFavTeacherView(LoginRequireMixin,View):
    """
    我收藏的授课讲师
    """
    def get(self,request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list': teacher_list
        })


class MyFavCourseView(LoginRequireMixin,View):
    """
    我收藏的课程
    """
    def get(self,request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=int(course_id))
            course_list.append(course)
        return render(request,'usercenter-fav-course.html',{
            'course_list': course_list
        })


class MyMessageView(LoginRequireMixin,View):
    """
    我的消息处理
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        # 如果消息多的话对消息进行分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages': messages
        })


class IndexView(View):
    """
    达内教育在线首页
    """
    def get(self,request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_course = Course.objects.filter(is_banner=False)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_course': banner_course,
            'course_orgs': course_orgs
        })


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def server_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html')
    response.status_code = 500
    return response



