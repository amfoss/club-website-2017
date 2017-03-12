# Django libraries
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

from register.forms import UpdateProfileForm, PasswordResetForm, RegistrationForm
from achievement.models import *
from images.models import ProfileImage
from fossWebsite.helper import error_key
from fossWebsite.helper import get_session_variables

# Python libraries
from django.views.generic import *
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect

# generic views
from django.views.generic import CreateView, UpdateView


class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = User_info

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(User_info.objects.make_random_password())
        obj.save()

        # This form only requires the "email" field, so will validate.
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        # Copied from django/contrib/auth/views.py : password_reset
        opts = {
            'use_https': self.request.is_secure(),
            'email_template_name': 'registration/verification.html',
            'subject_template_name': 'registration/verification_subject.txt',
            'request': self.request,
            # 'html_email_template_name': provide an HTML content template if you desire.
        }
        # This form sends the email on save()
        reset_form.save(**opts)

        return redirect('accounts:register-done')


class ProfileDetailView(DetailView):
    template_name = 'registration/profile.html'
    model = get_user_model()

    fields = ['firstname', 'lastname', 'gender', 'contact', 'role', 'blog_url', 'twitter_id',
              'topcoder_handle', 'github_id', 'bitbucket_id', 'typing_speed', 'interest',
              'expertise', 'goal']

    slug_field = 'username'


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


def mypage(request):
    """
    An editable profile page for the user
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/register/login')

    else:
        is_loggedin, username = get_session_variables(request)
        name = User_info.objects.get(username=username)
        return render(request, \
                      'register/mypages.html',
                      {'username': username, \
                       'firstname': name.firstname, \
                       'is_loggedin': is_loggedin, \
                       'lastname': name.lastname, }, \
                      RequestContext(request))


def update_profile_pic(request):
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/register/login')
        else:
            user_details = get_object_or_404(User_info, username=username)
            init_user_details = user_details.__dict__

            # If method is not POST
            if request.method != 'POST':
                # return form with old details
                return render(request, 'register/update_profile_pic.html',
                              {'form': UpdateProfileForm(init_user_details),
                               'is_loggedin': is_loggedin, 'username': username},
                              RequestContext(request))

            # If method is POST
            else:
                user_object = get_object_or_404(User_info, username=username)
                if 'image' in request.FILES:
                    try:
                        to_delete = ProfileImage.objects.filter(username=username)
                        for obj in to_delete:
                            obj.delete()
                    except ProfileImage.DoesNotExist:
                        pass
                    profile_image = request.FILES['image']
                    profile_image_object = ProfileImage(image=profile_image, username=user_object)
                    profile_image_object.image.name = username + ".jpg"
                    profile_image_object.save()
                redirect_url = "/register/profile/" + username + "/"
                return HttpResponseRedirect(redirect_url)

    except KeyError:
        return error_key(request)
