from django.conf.urls import url, include
from .views import AttendanceDetail, AttendanceList


urlpatterns = [
    url(r'^$', AttendanceList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', AttendanceDetail.as_view()),

    # browsable api django-rest framework

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
