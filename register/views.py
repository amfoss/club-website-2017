# Django libraries
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from register.forms import NewRegisterForm, UpdateProfileForm, PasswordResetForm, RegistrationForm
from register.forms import ChangePasswordForm
from achievement.models import *
from images.models import ProfileImage
from register.helper import sendmail_after_userreg
from register.helper import notify_new_user, sendmail_after_pass_change
from fossWebsite.helper import error_key
from fossWebsite.helper import get_session_variables

# Python libraries
from hashlib import sha512 as hash_func
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

    def get_object(self):
        return User_info.objects.get(username=self.request.user.username)


def profile(request, user_name=None):
    """
    A view to display the profile (public)
    """
    is_loggedin, username = get_session_variables(request)
    user_object = User_info.objects.get(username=request.user.username)

    profile_image_object = ProfileImage.objects.filter(username=user_object)

    user_email = user_object.email.replace('.', ' DOT ').replace('@', ' AT ')
    contributions = Contribution.objects.all().filter(username=user_name)[:3]
    articles = Article.objects.all().filter(username=user_name)[:3]
    gsoc = Gsoc.objects.all().filter(username=user_name)[:3]
    interns = Intern.objects.all().filter(username=user_name)[:3]
    speakers = Speaker.objects.all().filter(username=user_name)[:3]
    email = user_object.email
    icpc_achievement = ACM_ICPC_detail.objects.filter(participant1_email=email) | \
                       ACM_ICPC_detail.objects.filter(participant2_email=email) | \
                       ACM_ICPC_detail.objects.filter(participant3_email=email)
    print icpc_achievement
    if profile_image_object:
        image_name = user_name + ".jpg"
    else:
        image_name = "default_image.jpeg"

    return render(request, 'registration/profile.html', {'is_loggedin': is_loggedin, 'username': username,
                                                     'user_object': user_object, \
                                                     'user_email': user_email, \
                                                     'user_email': user_email, \
                                                     'gsoc': gsoc, \
                                                     'interns': interns, \
                                                     'speakers': speakers, \
                                                     'image_name': image_name, \
                                                     'articles': articles, \
                                                     'contributions': contributions, \
                                                     'icpc_achievement': icpc_achievement}, \
                  RequestContext(request))


def change_password(request):
    """
    A view to change the password of a logged in user
    """
    try:
        is_loggedin, username = get_session_variables(request)
        if not is_loggedin:
            return HttpResponseRedirect("/register/login")
        # POST request
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)

            # Form inputs are valid
            if form.is_valid():
                new_pass = request.POST['new_password']
                old_password = hash_func(request.POST['old_password']) \
                    .hexdigest()
                new_password = hash_func(request.POST['new_password']) \
                    .hexdigest()
                confirm_new_password = hash_func(
                    request.POST['confirm_new_password']) \
                    .hexdigest()

                user_data = User_info.objects.get(username=username)
                actual_pwd = user_data.password

                # Given current and stored passwords same
                if old_password == actual_pwd:
                    # New and current passwords user provided are not same
                    if new_password != actual_pwd:
                        # Repass and new pass are same
                        if new_password == confirm_new_password:
                            user_data.password = new_password
                            sendmail_after_pass_change( \
                                username, \
                                new_pass, \
                                user_data.email)
                            user_data.save()
                            return render(request, \
                                          'register/pass_success.html',
                                          {'username': username, \
                                           'is_loggedin': is_loggedin}, \
                                          RequestContext(request))
                        # Repass and new pass are not same
                        else:
                            error = "New passwords doesn't match"
                            return render(request, \
                                          'register/change_password.html',
                                          {'form': form, \
                                           'username': username, \
                                           'is_loggedin': is_loggedin, \
                                           'error': error}, \
                                          RequestContext(request))
                    # New and current password user provided are same
                    else:
                        error = "Your old and new password are same. Please \
                                choose a different password"
                        return render(request, \
                                      'register/change_password.html',
                                      {'form': form, \
                                       'username': username, \
                                       'is_loggedin': is_loggedin, \
                                       'error': error}, \
                                      RequestContext(request))
                # Given current and stored passwords are not same
                else:
                    error = "Current password and given password doesn't match"
                    return render(request, \
                                  'register/change_password.html',
                                  {'form': form, \
                                   'username': username, \
                                   'is_loggedin': is_loggedin, \
                                   'error': error}, \
                                  RequestContext(request))
            # Form inputs is/are invalid
            else:
                form = ChangePasswordForm()

            return render(request, \
                          'register/change_password.html',
                          {'form': form, \
                           'username': username, \
                           'is_loggedin': is_loggedin}, \
                          RequestContext(request))

        return render(request, \
                      'register/change_password.html',
                      {'username': username, \
                       'is_loggedin': is_loggedin}, \
                      RequestContext(request))

    except KeyError:
        return error_key(request)


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

