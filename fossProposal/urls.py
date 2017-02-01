from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add/', views.ProposalCreate.as_view(), name='proposal_add'),
    url(r'^$', views.ProposalListView.as_view(), name="proposal-list"),
]