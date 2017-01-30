from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add/', views.proposal_add, name='proposal_add'),
    url(r'^$', views.ProposalListView.as_view(), name="proposal-list"),
]