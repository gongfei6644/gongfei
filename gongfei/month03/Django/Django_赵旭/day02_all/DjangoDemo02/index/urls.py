from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index_views),
    url(r'^index/$',views.index_views),
    url(r'^login/$',views.login_views),
    url(r'^register/$',views.register_views),
]

urlpatterns += [
    url(r'^01-temp/$',views.temp_views),
    url(r'^02-var1/$',views.var1_views),
    url(r'^03-var2/$',views.var2_views),
    url(r'^04-tag/$',views.tag_views),
    url(r'^05-static/$',views.static_views),
]

