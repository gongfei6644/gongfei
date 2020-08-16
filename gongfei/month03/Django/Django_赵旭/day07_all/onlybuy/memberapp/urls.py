from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^goodetail/$',views.goodetail_views),
]