from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^01-request/$',views.request_views),
    url(r'^02-get/$',views.get_views),
    url(r'^03-post/$',views.post_views),
    url(r'^04-register/$',views.register_views),
    url(r'^05-form/$',views.form_views),
    url(r'^06-register',views.reg06_views),
    url(r'^07-login/$',views.login_views),
    url(r'^08-info/$',views.info_views),
]