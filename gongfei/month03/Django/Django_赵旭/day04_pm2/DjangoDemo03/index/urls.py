from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^01-parent/$',views.parent_views),
    url(r'^02-child/$',views.child_views),
]

urlpatterns = [
    url(r'^03-create/$',views.create_views),
    url(r'^04-retrieve/$',views.retrieve_views),
    url(r'^05-filter/$',views.filter_views),
    url(r'^06-filter-exer/$',views.filterexer_views),
    url(r'^07-exclude/$',views.exclude_views),
    url(r'^08-get/$',views.get_views),
    url(r'^09-aggregate/$',views.aggregate_views),
    url(r'^10-queryall/$',views.queryall_views),
    url(r'^11-querybyid/(\d+)/$',views.querybyid_views),
    url(r'^12-delete/(\d+)/$',views.delete_views),
    url(r'^13-updateall/$',views.updateall_views),
]








