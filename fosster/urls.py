from django.conf.urls import url

from fosster.views import AuthorCreate, ThankYou

urlpatterns = [
    url(r'^$', AuthorCreate.as_view(), name='coming_soon'),
    url(r'^thank_you$', ThankYou.as_view(), name='thank-you'),
]