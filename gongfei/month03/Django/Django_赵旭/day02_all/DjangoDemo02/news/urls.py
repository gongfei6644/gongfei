from django.conf.urls import url
from . import views

# 进入到该urls.py 相当于已经匹配到了 http://127.0.0.1:8000/index/ 地址了,所以在该文件中要继续匹配剩余的访问路径
urlpatterns = [
    #匹配:http://127.0.0.1:8000/news/show/
    #只需要匹配到 show/ 即可
    url(r'^show/$',views.show_views),
]