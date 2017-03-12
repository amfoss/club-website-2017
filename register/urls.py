from django.conf.urls import *
from register import views
from register.views import ResetSuccess, ChangePasswordView

urlpatterns = [
    url(r'^new/$', views.newregister),
    url(r'^mypage/$', views.mypage),
    url(r'^profile/(?P<user_name>\w+)/$',views.profile),
    url(r'^update_profile/$',views.update_profile),
    url(r'^update_profile_pic/$', views.update_profile_pic),
    url(r'^change_password', ChangePasswordView.as_view(), name='change_password'),
    url(r'^reset_success', ResetSuccess.as_view(), name='password_reset_success'),
]
