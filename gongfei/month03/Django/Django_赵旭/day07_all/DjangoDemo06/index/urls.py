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

urlpatterns += [
    url(r'^09-cookie/$',views.cookie_views),
    url(r'^10-setsession/$',views.setsession_views),
    url(r'^11-getsession/$',views.getsession_views),
    url(r'^12-server/$',views.server12_views),
    url(r'^12-json/$',views.json_views),
    url(r'^12-json-users/$',views.json_users),
    url(r'^13-ajax-post/$',views.json_post),
    url(r'^13-server/$',views.server13_views),
]











