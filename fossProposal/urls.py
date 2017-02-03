from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ProposalListView.as_view(), name="proposal-list"),
    url(r'^add/', views.ProposalCreateView.as_view(), name='proposal_add'),
    url(r'^(?P<pk>\d+)/update/', views.ProposalUpdateView.as_view(), name='proposal_update'),
    url(r'^(?P<pk>[-\w]+)/$', views.ProposalDetailView.as_view(), name="proposal-detail"),
]