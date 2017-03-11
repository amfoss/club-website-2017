from django.conf.urls import url

from fosster.views import ComingSoon, ThankYou

urlpatterns = [
    url(r'^$', ComingSoon.as_view(), name='coming_soon'),
    url(r'^thank_you$', ThankYou.as_view(), name='thank-you'),
]