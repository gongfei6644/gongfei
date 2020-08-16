from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^addcart/$',views.addcart_views),
  url(r'^cartlist/$',views.cartlist_views),
]