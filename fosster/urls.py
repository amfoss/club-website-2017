from django.conf.urls import url

from fosster.views import CommingSoon

urlpatterns = [
    url(r'$', CommingSoon.as_view(), name='coming_soon'),
]