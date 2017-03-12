from django.conf.urls import *
from register import views
from register.views import ResetPasswordRequestView, PasswordResetConfirmView

urlpatterns = [
    # url(r'^login/$', views.login, name='login'),
    url(r'^password_change_success/$', views.password_change_success, name='password_change_success'),
    # url(r'^logout/$', views.logout),
    url(r'^new/$', views.newregister),
    url(r'^mypage/$', views.mypage),
    url(r'^profile/(?P<user_name>\w+)/$',views.profile),
    url(r'^update_profile/$',views.update_profile),
    url(r'^update_profile_pic/$',views.update_profile_pic),
]


