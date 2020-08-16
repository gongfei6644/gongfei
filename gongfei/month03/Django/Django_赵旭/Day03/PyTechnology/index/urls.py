from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index_views),
    url(r'^cart/$',views.cart_views),
    url(r'^login/$',views.login_views),
]