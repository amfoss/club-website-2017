from django.conf.urls import *
from register import views
from register.views import UpdateProfileView, ProfileDetailView

urlpatterns = [
    url(r'^mypage/$', views.mypage, name='my-page'),
    url(r'^profile/(?P<slug>[\w-]+)/$', ProfileDetailView.as_view(), name='profile'),
    url(r'^update/profile$', UpdateProfileView.as_view(), name='profile-update'),
    url(r'^update/profile/pic/$', views.update_profile_pic, name='profile-pic-update'),
]
