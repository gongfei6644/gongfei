from django.shortcuts import render
from django.http import HttpResponse

from index.models import Users
from .forms import *

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







