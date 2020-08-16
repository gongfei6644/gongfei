from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index_views(request):
    return HttpResponse("这是music应用中的index视图")
