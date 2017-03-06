from django.conf.urls import *
from register import views
from register.views import ResetPasswordRequestView

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout),
    url(r'^new/$', views.newregister),
    url(r'^mypage/$', views.mypage),
    url(r'^profile/(?P<user_name>\w+)/$',views.profile),
    url(r'^update_profile/$',views.update_profile),
    url(r'^update_profile_pic/$',views.update_profile_pic),

    url(r'^forpass/$', ResetPasswordRequestView.as_view(), name="reset_password"),

]


