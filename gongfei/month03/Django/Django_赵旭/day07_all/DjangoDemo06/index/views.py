import json

from django.shortcuts import render
from django.http import HttpResponse

from index.models import Users
from .forms import *
from django.core import serializers

# Create your views here.
def request_views(request):
    print(dir(request))
    return HttpResponse("request查询成功")

def get_views(request):
    # 从地址栏中传入 uname 和 uage 的参数
    if 'uname' in request.GET:
        uname = request.GET['uname']
        print("uname:"+uname)
    if 'uage' in request.GET:
        uage = request.GET['uage']
        print("uage:"+uage)
    return HttpResponse("get请求成功!")


def post_views(request):
    if request.method == 'GET':
        return render(request,'03-post.html')
    else:
        uname = request.POST['uname']
        uage = request.POST['uage']
        return HttpResponse("uname:%s,uage:%s" % (uname,uage))

def register_views(request):
    if request.method == 'GET':
        return render(request,'04-register.html')
    else:
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        hobby = request.POST.getlist('hobby')
        jiguan = request.POST.get('jiguan')

        print(name,age,gender,hobby,jiguan)

        return HttpResponse("注册成功")

def form_views(request):
    if request.method == 'GET':
        form = RemarkForm()
        return render(request,'05-form.html',locals())
    else:
        #1.将request.POST的数据交给RemarkForm()
        form = RemarkForm(request.POST)
        #2.使得form通过验证 -is_valid()
        if form.is_valid():
            #3.获取表单中的值 - cleaned_data
            data = form.cleaned_data
            print(data)
        return HttpResponse("获取数据成功")


def reg06_views(request):
    if request.method == 'GET':
        #1.创建RegisterForm对象
        form = RegisterForm()
        #2.将form对象发送到06-register.html模板上
        return render(request,'06-register.html',locals())
    else:
        #1.将request.POST交给RegisterForm
        form = RegisterForm(request.POST)
        #2.判断form是否通过验证 - is_valid()
        if form.is_valid():
            #3.获取数据 - cleaned_data
            data = form.cleaned_data
            user = Users(**data)
            user.save()
        return HttpResponse("注册成功")

def login_views(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'07-login.html',locals())


def info_views(request):
    form = InfoForm()
    return render(request,'08-info.html',locals())

def cookie_views(request):
    if request.method == 'GET':
        #First : check uname and id in cookie
        if 'id' in request.COOKIES and 'uname' in request.COOKIES:
            uname = request.COOKIES['uname']
            return HttpResponse("Welcome:"+uname)
        return render(request,'09-cookie.html')
    else:
        uname = request.POST['uname']
        upwd = request.POST['upwd']
        duration = request.POST['duration']

        users = Users.objects.filter(uname=uname,upwd=upwd)

        if users:
            resp = HttpResponse("Login OK")
            duration = int(duration)
            max_age = 0
            if duration == 1:
                max_age = 60 * 60 * 24 * 30
            elif duration == 2:
                max_age = 60 * 60 * 24 * 30 * 6
            elif duration == 3:
                max_age = 60 * 60 * 24 * 365
            resp.set_cookie('id',users[0].id,max_age)
            resp.set_cookie('uname',uname,max_age)
            return resp
        else:
            return HttpResponse("用户名或密码不正确")

def setsession_views(request):
    request.session['uname'] = "lvzeMaria"
    request.session['upwd'] = '123456'
    return HttpResponse("Set session success!")

def getsession_views(request):
    uname = request.session.get('uname',"Unknown")
    upwd = request.session.get('upwd','Unknown')
    return HttpResponse("Username:%s,Userpwd:%s" % (uname,upwd))


def server12_views(request):
    # recevied front params
    uname = request.GET['uname']
    uage = request.GET['uage']
    return HttpResponse("UNAME:%s,UAGE:%s" % (uname,uage))

def json_views(request):
    person = {
        'name':'lvzemaria',
        'age' : 30,
        'gender' : 'male',
        'email' : 'maria@163.com',
    }
    personStr = json.dumps(person)
    return HttpResponse(personStr)

def json_users(request):
    users = Users.objects.all()
    # QuerySet can use this method
    # users must a QuerySet
    jsonStr = serializers.serialize('json',users)
    return HttpResponse(jsonStr)



def server13_views(request):
    uname = request.POST['uname']
    upwd = request.POST['upwd']

    return HttpResponse("注册信息为:%s,%s" % (uname,upwd))


def json_post(request):
    return render(request,'13-ajax-post.html')




