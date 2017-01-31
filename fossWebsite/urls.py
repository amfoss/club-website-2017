from django.conf.urls import *
from fossWebsite import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home),
    url(r'^search/', views.search),
    url(r'^contact/', views.contact),
    url(r'^register/', include('register.urls')),
    url(r'^achievement/', include('achievement.urls')),
    url(r'^images/', include('images.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^proposal/', include('fossProposal.urls'), name='foss-proposals')
]
