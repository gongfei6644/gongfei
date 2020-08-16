from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^01-parent/$',views.parent_views),
    url(r'^02-child/$',views.child_views),
]