from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$',views.index_views),
  url(r'^footer/$',views.footer_views),
  url(r'^header/$',views.header_views),
  url(r'^product_details/$',views.product_details),
]