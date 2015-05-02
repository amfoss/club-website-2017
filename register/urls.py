from django.conf.urls import *
from register import views

urlpatterns = patterns('',
    url(r'^/login/$', views.login),
    url(r'^/logout/$', views.logout),
    #url(r'^/new/$', views.newregister),
    url(r'^/mypage/$', views.mypage),
    url(r'^/change_password/$', views.change_password),
    url(r'^/profile/(?P<user_name>\w+)/$',views.profile),
    url(r'^/update_profile/$',views.update_profile),
    url(r'^/update_profile_pic/$',views.update_profile_pic),
)
