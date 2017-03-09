from django.conf.urls import *
from register import views
from register.views import ResetPasswordRequestView, PasswordResetConfirmView

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^password_change_success/$', views.password_change_success, name='password_change_success'),
    url(r'^logout/$', views.logout),
    url(r'^new/$', views.newregister),
    url(r'^mypage/$', views.mypage),
    url(r'^profile/(?P<user_name>\w+)/$',views.profile),
    url(r'^update_profile/$',views.update_profile),
    url(r'^update_profile_pic/$',views.update_profile_pic),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='reset_password_confirm'),
    url(r'^forpass/$', ResetPasswordRequestView.as_view(), name="reset_password"),
    url(r'^change_password/$', PasswordResetConfirmView.as_view(), name="change_password"),

]


