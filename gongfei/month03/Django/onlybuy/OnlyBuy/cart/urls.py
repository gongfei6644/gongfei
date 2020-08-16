from django.conf.urls import url
from . import views
urlpatterns = [
    url('^add/$',views.add_cart),
    url('^$',views.list_all),
    url('^delete/(?P<id>\d+)/$',views.delete)


]