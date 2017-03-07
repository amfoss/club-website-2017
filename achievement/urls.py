from django.conf.urls import *
from achievement import views

urlpatterns = [
    url(r'^viewall/$',views.achieve_viewall),
    url(r'^contribution/$', views.contrib_viewall),
    url(r'^articles/$', views.article_viewall),
    url(r'^gsoc/$', views.gsoc_viewall),
    url(r'^speakers/$', views.speaker_viewall),
    url(r'^interns/$', views.intern_viewall),
    url(r'^contests/$', views.contest_won_viewall),
    url(r'^icpc/$', views.icpc_viewall),

    url(r'^new/contribution/$', views.insert_contribution),
    url(r'^new/article/$', views.insert_article),
    url(r'^new/talk/$', views.insert_talk),
    url(r'^new/gsoc/$', views.insert_gsoc),
    url(r'^new/intern/$', views.insert_intern),
    url(r'^new/icpc/$', views.insert_icpc),

    url(r'^contribution/update/(?P<achievement_id>\w+)/$',views.update_contribution),
    url(r'^article/update/(?P<achievement_id>\w+)/$',views.update_article),
    url(r'^intern/update/(?P<achievement_id>\w+)/$',views.update_intern),
]
