from django.conf.urls import url
from userinfo import views
urlpatterns = [
    url(r'registerin/',views.register_,name="register_in"),
]

