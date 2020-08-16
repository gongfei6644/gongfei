from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def temp_views(request):

    # 方案1:使用loader对象加载模板
    #1. 加载模板
    # t = loader.get_template("01-temp.html")
    #2. 渲染成字符串并响应
    # return HttpResponse(t.render())

    #2. 使用render函数加载模板
    return render(request,'01-temp.html')

def var1_views(request):
    #1.声明变量
    # dic = {
    #     "uname" : "吕泽Maria",
    #     "age" : 30,
    #     "salary" : "50000"
    # }

    uname = "吕泽Maria"
    age = 30
    salary = 50000

    t = loader.get_template('02-var1.html')
    html = t.render(locals())
    return HttpResponse(html)

def var2_views(request):
    uname = "吕泽Maria"
    age = 30
    salary = 50000
    hobby = ["保健","保健","大保健"]
    foods = ("大肠刺身","小肠刺身","各种刺身")
    films = {
        "MSN" : "美少女战士",
        "XMX" : "巴拉巴拉小魔仙"
    }
    animal = Animal()
    animal.name = "吕三多"

    return render(request,'03-var2.html',locals())

def tag_views(request):
    list = ["潘金莲","李世时","李白","鲁班七号"]
    return render(request,'04-tag.html',locals())

def static_views(request):
    return render(request,'05-static.html')






class Animal(object):
    name = "旺财",
    def eat(self):
        return self.name + "正在吃饭!"













def index_views(request):
    return HttpResponse("这是index应用中的index_views")

def login_views(request):
    return HttpResponse('这是index应用中的login_views')

def register_views(request):
    return HttpResponse('这是index应用中的register_views')

