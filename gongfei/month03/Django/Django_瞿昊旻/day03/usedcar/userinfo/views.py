from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from .models import UserInfo
from django.contrib import auth
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import UserInfoSerializer
from .permissions import *
# Create your views here.
def register_(request):
    if request.method == "POST":
        username = request.POST.get("username","")
        olduser = UserInfo.objects.filter(username = username)
        if olduser:
            return render(request,'register.html',{'msg':'用户名重复'})

        pwd = request.POST.get("pwd","")
        cpwd = request.POST.get("cpwd","")
        if pwd != cpwd:
            return render(request,'register.html',{'msg':'密码不一致'})
        password = make_password(pwd,None,'pbkdf2_sha1')
        # check_password('','')
        UserInfo.objects.create(username=username,password=password)
        # UserInfo.objects.create()
        # .save()
        # UserInfo.objects.update()
        return render(request,'login.html',{"msg":'注册成功'})

    elif request.method == "GET":
        pass

def login_(request):
    if request.method == "POST":
        new_user = UserInfo()
        new_user.username = request.POST.get("username","")
        new_user.password = request.POST.get("password","")
        user = auth.authenticate(username=new_user.username,password=new_user.password)
        if user is not None and user.is_active:
            auth.login(request,user)
            if request.COOKIES.get("source_url"):
                url=request.COOKIES.get("source_url")
                res = redirect(url)
                res.delete_cookie('source_url')
                return res


            return render(request,'index.html',{"msg":"登录成功"})


        pass
    elif request.method == "GET":
        # 查询id第３３－４４的用户（分页）
        UserInfo.objects.filter(id__gt=32,id__lt=45)
        UserInfo.objects.filter(id__range=(33,44))
        pass


def logout_(request):
    auth.logout(request)
    return redirect('/')



class UserList(APIView):

    permission_classes = (
        IsSuper,
    )

    def post(self,request):
        users = UserInfo.objects.all()
        user_data = UserInfoSerializer(users, many=True)
        data = user_data.data
        return JsonResponse({'result':True,"data":data,"error":"用户名错误"})
        {'result': True, "data": [{"username":"python","email":"aa@aa.com"},{"username":"python2","email":"aa2@aa.com"}], "error": "用户名错误"}

    def get(self,request):
        pass

    def delete(self, request):
        request.data.get('')

    def put(self,request):
        pass







