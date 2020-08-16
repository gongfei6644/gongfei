"""mxproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin
from users.views import *
from organization.views import OrgView
from mxproject.settings import MEDIA_ROOT
from users.views import LogoutView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$',IndexView.as_view(), name='index'),

    # url('^login/$',TemplateView.as_view(template_name='login.html'),name='login'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),

    # 此方法可以将active之后的所有的内容提出出来绑定到active_code中
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^reset/(?P<active_code>.*)/$', ResetUserView.as_view(), name='reset_pwd'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 配置文件上传的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 课程机构url配置,url的转换和分发
    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程相关url配置,url的转换和分发
    url(r'^course/', include('courses.urls', namespace='course')),

    # 配置上传文件的访问处理函数

    # 个人信息相关的路由
    url(r'^users/', include('users.urls',namespace='users')),
    # 退出登录
    url('^logout/$', LogoutView.as_view(), name='logout'),

    # 配置静态文件处理函数
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    # 富文本编辑器
    url(r'^ueditor/', include('DjangoUeditor.urls'))

]

# 全局404 页面配置
handler404 = 'users.views.page_not_found'
# 全局500 页面配置
handler500 = 'users.views.server_error'
