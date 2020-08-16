# HttpResponse 在Django中能够向客户端浏览器响应一段文本
from django.http import HttpResponse

def show_views(request):
    """
    处理业务的视图处理函数
    :param request: 表示的是本次请求的请求对象,封装了请求中所有的信息
    :return: 要响应给客户端的内容
    """
    return HttpResponse("这是我的第一个Django程序")

def login_views(request):
    return HttpResponse("这是登录页面")

def register_views(request):
    name = 'Teacher Lv'
    return HttpResponse("姓名:%s" % name)

def show_test(request):
    return HttpResponse("这是show_test视图处理函数")


# http://127.0.0.1:8000/02-url/四位数字
def url_views(request,year):
    return HttpResponse("传递进来的年份为:" + year)

#http://127.0.0.1:8000/03-url/四位数字/1-2位数字/1-2位数字
def url03_views(request,year,month,day):
    return HttpResponse("生日:%s年%s月%s日" % (year,month,day))

#访问路径:/04-url/两位及以上的非空白字符/1-2位数字
def url04_views(request,name,age):
    return HttpResponse("姓名:%s,年龄:%s" % (name,age))






