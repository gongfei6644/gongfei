from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def show_views(request):
    return HttpResponse("这是index应用中的show的访问路径")
