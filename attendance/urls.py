from django.conf.urls import url, include
from . import views


urlpatterns = [
    # browsable api django-rest framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]