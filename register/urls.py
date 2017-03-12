from django.conf.urls import *
from register import views
from register.views import UpdateProfileView, ProfileDetailView, StudentDetailView, StudentCreateView, \
    UpdateStudentDetailView

urlpatterns = [
    url(r'^mypage/$', views.mypage, name='my-page'),
    url(r'^profile/$', ProfileDetailView.as_view(), name='profile'),
    url(r'^profile/(?P<slug>[\w-]+)/$', ProfileDetailView.as_view(), name='profile'),
    url(r'^update/profile$', UpdateProfileView.as_view(), name='profile-update'),
    url(r'^update/profile/pic/$', views.update_profile_pic, name='profile-pic-update'),

    url(r'^student/profile/$', StudentDetailView.as_view(), name='student-data'),
    url(r'^student/profile/(?P<slug>[\w-]+)/$', StudentDetailView.as_view(), name='student-data'),
    url(r'^student/add/profile/$', StudentCreateView.as_view(), name='student-data'),
    url(r'^student/update/profile/$', UpdateStudentDetailView.as_view(), name='update-student-data'),
]
