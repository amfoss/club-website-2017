from django.conf.urls import *
from django.contrib import auth
from registration.backends.hmac.views import RegistrationView
from fossWebsite import views
from django.contrib import admin
from register.forms import CustomRegisterUserForm

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # url('^accounts/', include('django.contrib.auth.urls')),
    # url(r'^login/$', auth.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^search/', views.search),
    url(r'^contact/', views.contact),
    url(r'^register/', include('register.urls')),
    url(r'^achievement/', include('achievement.urls')),
    url(r'^images/', include('images.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^proposal/', include('fossProposal.urls'), name='foss-proposals'),
    url(r'^attendance/', include('attendance.urls'), name='attendance'),
    url(r'fosster/', include('fosster.urls'), name='fosster'),
    url(r'^accounts/register/$',
            RegistrationView.as_view(
                form_class=CustomRegisterUserForm
            ),
            name='registration_register',
        ),
    url(r'^accounts/', include('registration.backends.hmac.urls'), name='accounts'),
]
