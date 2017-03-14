from django.conf.urls import *
from django.contrib.auth.decorators import login_required

from register import views
from register.views import UpdateProfileView, ProfileDetailView, StudentDetailView, StudentCreateView, \
    UpdateStudentDetailView

urlpatterns = [
    url(r'^mypage/$', views.mypage, name='my-page'),
    url(r'^profile/$', ProfileDetailView.as_view(), name='profile'),
    url(r'^profile/(?P<slug>[\w-]+)/$', ProfileDetailView.as_view(), name='profile'),
    url(r'^update/profile/$', login_required(UpdateProfileView.as_view()), name='profile-update'),

    url(r'^student/profile/$', login_required(StudentDetailView.as_view()), name='student-data'),
    url(r'^student/profile/(?P<slug>[\w-]+)/$', login_required(StudentDetailView.as_view()), name='student-data'),
    url(r'^student/add/profile/$', login_required(StudentCreateView.as_view()), name='student-data'),
    url(r'^student/update/profile/$', login_required(UpdateStudentDetailView.as_view()), name='update-student-data'),
]
