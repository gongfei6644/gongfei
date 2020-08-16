from django.shortcuts import render

# Create your views here.
def index_views(request):
    return render(request,'index.html')

def cart_views(request):
    return render(request,'cart.html')

def login_views(request):
    return render(request,'login.html')