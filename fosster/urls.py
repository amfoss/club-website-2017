from django.conf.urls import url

from fosster.views import ComingSoon

urlpatterns = [
    url(r'$', ComingSoon.as_view(), name='coming_soon'),
]