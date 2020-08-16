from django.shortcuts import render

# Create your views here.
def parent_views(request):
    uname = "吕泽Maria"
    return render(request,'01-parent.html',locals())

def child_views(request):
    uname = "小泽老师"
    return render(request,'02-child.html',locals())