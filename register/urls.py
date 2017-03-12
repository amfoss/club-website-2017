from django.conf.urls import *
from register import views
from register.views import UpdateProfileView

urlpatterns = [
    url(r'^mypage/$', views.mypage, name='my-page'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/update/$', UpdateProfileView.as_view(), name='profile-update'),
    url(r'^profile/pic/update/$', views.update_profile_pic, name='profile-pic-update'),
]
