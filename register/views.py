# Django libraries
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from achievement.models import *
from images.models import ProfileImage
from fossWebsite.helper import error_key
from fossWebsite.helper import get_session_variables

# Python libraries
from django.views.generic import *

# generic views
from django.views.generic import CreateView, UpdateView
from register.models import Student


class ProfileDetailView(DetailView):
    template_name = 'registration/profile.html'
    model = get_user_model()

    fields = ['firstname', 'lastname', 'gender', 'contact', 'role', 'blog_url', 'twitter_id',
              'topcoder_handle', 'github_id', 'bitbucket_id', 'typing_speed', 'interest',
              'expertise', 'goal']

    slug_field = 'username'

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if slug is None:
            slug = self.request.user.username

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/update_profile.html'
    model = get_user_model()
    fields = ['firstname', 'lastname', 'gender', 'contact', 'role', 'blog_url', 'twitter_id',
              'topcoder_handle', 'github_id', 'bitbucket_id', 'typing_speed', 'interest',
              'expertise', 'goal']

    success_message = 'Your settings have been saved.'
    success_url = '/register/profile/'

    def get_object(self):
        return User_info.objects.get(username=self.request.user.username)


class StudentDetailView(DetailView):
    template_name = 'registration/student_profile.html'
    model = Student

    fields = ['username', 'roll_number', 'branch', 'year', 'cgpa', 'mentors', 'system_number', 'responsibility1',
              'responsibility2', 'responsibility3', 'responsibility4', 'responsibility5', 'responsibility_count',
              'comments', ]

    slug_field = 'username'

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if slug is None:
            slug = self.request.user.username

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class UpdateStudentDetailView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/student_profile_form.html'
    model = Student
    fields = ['roll_number', 'branch', 'year', 'cgpa', 'mentors', 'system_number', 'responsibility1',
              'responsibility2', 'responsibility3', 'responsibility4', 'responsibility5', 'responsibility_count',
              'comments', ]

    success_message = 'Your settings have been saved.'
    success_url = '/register/student/profile/'

    def get_object(self):
        return Student.objects.get(username=self.request.user.username)


class StudentCreateView(CreateView):
    template_name = 'registration/student_profile_form.html'
    model = Student
    success_url = '/register/student/profile/'

    fields = ['roll_number', 'branch', 'year', 'cgpa', 'mentors', 'system_number', 'responsibility1',
              'responsibility2', 'responsibility3', 'responsibility4', 'responsibility5', 'responsibility_count',
              'comments', ]

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super(StudentCreateView, self).form_valid(form)


def mypage(request):
    """
    An editable profile page for the user
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/register/login')

    else:
        is_loggedin, username = get_session_variables(request)
        name = User_info.objects.get(username=username)
        return render(request,
                      'register/mypages.html',
                      {'username': username,
                       'firstname': name.firstname,
                       'is_loggedin': is_loggedin,
                       'lastname': name.lastname, },
                      RequestContext(request))


