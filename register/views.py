# Django libraries
from django.contrib.auth import get_user_model
from django.template import RequestContext, context
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect

from register.forms import LoginForm, NewRegisterForm, UpdateProfileForm, SetPasswordForm, PasswordResetForm
from register.forms import ChangePasswordForm
from achievement.models import *
from images.models import ProfileImage
from register.helper import sendmail_after_userreg
from register.helper import notify_new_user, sendmail_after_pass_change
from fossWebsite.helper import error_key, logged_in
from fossWebsite.helper import get_session_variables

# Python libraries
from hashlib import sha512 as hash_func

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from django.views.generic import *
from .forms import PasswordResetRequestForm
from django.contrib import messages
from django.db.models.query_utils import Q


# Using django in build login and logout.

# def login(request):
#     """
#     A view to evaluate login form
#     """
#     try:
#         # If the user is already loggedin never show the login page
#         if request.user.is_authenticated():
#             return render(request, 'register/logged_in.html', {})
#
#         # Upon signin button click
#         if request.method == 'POST':
#             form = LoginForm(request.POST)
#
#             # Form has all valid entries
#             if form.is_valid():
#                 cleaned_login_data = form.cleaned_data
#                 inp_username = cleaned_login_data['username']
#                 inp_password = cleaned_login_data['password']
#                 hashed_password = hash_func(inp_password).hexdigest()
#                 user_tuple = User_info.objects.all().filter(username=inp_username)
#
#                 # There exist an entry in table with the given username
#                 if user_tuple:
#                     actual_pwd = user_tuple[0].password
#
#                     # Password matches: session validation
#                     if actual_pwd == hashed_password:
#                         request.session['is_loggedin'] = True
#                         request.session['username'] = inp_username
#                         request.session['email'] = user_tuple[0].email
#                         return HttpResponseRedirect('/')
#
#                     # Invalid password
#                     else:
#                         error = "Invalid password. Is it really you, " + \
#                                 str(inp_username) + "?"
#                         return render(request, 'register/login.html', \
#                                       {'form': form, 'error': error})
#
#                 # There's no entry in the table with the given username
#                 else:
#                     error = "User doesn't exist!"
#                     return render(request, 'register/login.html', \
#                                   {'form': form, 'error': error})
#
#             # Invalid form inputs
#             else:
#                 error = "Invalid username and password"
#                 return render(request, 'register/login.html',
#                               {'form': form, 'error': error}, )
#
#         # 'GET' request i.e refresh
#         else:
#             # User is logged in and hence redirect to home page
#             if 'is_loggedin' in request.session and \
#                     request.session['is_loggedin']:
#                 return HttpResponseRedirect('/')
#             # User is not logged in and refresh the page
#             else:
#                 form = LoginForm()
#
#         return render(request, 'register/login.html',
#                       {'form': form})
#
#     except KeyError:
#         return error_key(request)


# def logout(request):
#     """
#     A view to handle logout request
#     """
#     try:
#         del request.session['is_loggedin']
#         del request.session['username']
#         request.session.flush()
#         return render_to_response('register/logout.html', RequestContext(request))
#     except KeyError:
#         pass
#
#
# def forpass(request):
#     try:
#         return render(request, 'register/forpass.html', {'context': context})
#     except KeyError:
#         pass


def newregister(request):
    """
    Make a new registration, inserting into User_info and
    ProfileImage models.
    """
    try:
        # If the user is already loggedin never show the login page
        if request.user.is_authenticated():
            return render(request, 'register/logged_in.html', {})

        # Upon Register button click
        if request.method == 'POST':
            form = NewRegisterForm(request.POST, request.FILES)

            # Form has all valid entries
            if form.is_valid():
                cleaned_reg_data = form.cleaned_data
                inp_username = cleaned_reg_data['username']
                inp_password = cleaned_reg_data['password']
                inp_email = cleaned_reg_data['email']

                # Saving the user inputs into table
                new_register = form.save(commit=False)
                new_register.password = hash_func(inp_password) \
                    .hexdigest()
                new_register.save()

                user_object = get_object_or_404(User_info, \
                                                username=inp_username)

                # # Optional image upload processing and saving
                # if 'image' in request.FILES:
                #     profile_image = request.FILES['image']
                #     profile_image_object = ProfileImage \
                #         (image=profile_image, \
                #          username=user_object)
                #     profile_image_object.image.name = inp_username + \
                #                                       ".jpg"
                #     profile_image_object.save()

                # Setting the session variables
                request.session['username'] = cleaned_reg_data['username']
                request.session['is_loggedin'] = True
                request.session['email'] = cleaned_reg_data['email']
                sendmail_after_userreg(inp_username, inp_password, inp_email)
                notify_new_user(inp_username, inp_email)
                return render(request, 'register/register_success.html',
                              {'is_loggedin': request.user.is_authenticated(), \
                               'username': request.session['username']}, )

            # Invalid form inputs
            else:
                error = "Invalid inputs"
                return render(request, 'register/newregister.html',
                              {'form': form, 'error': error},
                              RequestContext(request))

        return render(request, 'register/newregister.html',
                      {'form': NewRegisterForm})

    except KeyError:
        return error_key(request)


def profile(request, user_name):
    """
    A view to display the profile (public)
    """
    is_loggedin, username = get_session_variables(request)
    user_object = get_object_or_404(User_info, \
                                    username=user_name)
    profile_image_object = ProfileImage.objects \
        .filter(username=user_object)
    user_email = user_object.email.replace('.', ' DOT ') \
        .replace('@', ' AT ')
    contributions = Contribution.objects.all() \
                        .filter(username=user_name)[:3]
    articles = Article.objects.all() \
                   .filter(username=user_name)[:3]
    gsoc = Gsoc.objects.all() \
               .filter(username=user_name)[:3]
    interns = Intern.objects.all() \
                  .filter(username=user_name)[:3]
    speakers = Speaker.objects.all() \
                   .filter(username=user_name)[:3]
    email = user_object.email
    icpc_achievement = ACM_ICPC_detail.objects.filter(participant1_email=email) | \
                       ACM_ICPC_detail.objects.filter(participant2_email=email) | ACM_ICPC_detail.objects.filter(
        participant3_email=email)
    print icpc_achievement
    if profile_image_object:
        image_name = user_name + ".jpg"
    else:
        image_name = "default_image.jpeg"

    return render(request, \
                  'register/profile.html', \
                  {'is_loggedin': is_loggedin, \
                   'username': username, \
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


def update_profile(request):
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
                return render(request, 'register/update_profile.html', \
                              {'form': UpdateProfileForm(init_user_details), \
                               'is_loggedin': is_loggedin, 'username': username}, \
                              RequestContext(request))

            # If method is POST
            else:
                profile_update_form = UpdateProfileForm(request.POST)
                # Form is not valid
                if not profile_update_form.is_valid():
                    # return form with old details

                    print profile_update_form.cleaned_data
                    return render(request, 'register/update_profile.html', \
                                  {'form': UpdateProfileForm(init_user_details), \
                                   'is_loggedin': is_loggedin, 'username': username}, \
                                  RequestContext(request))
                    # Form is valid:
                else:
                    user_details_form = profile_update_form.save(commit=False)
                    user_details_obj = get_object_or_404(User_info, username=username)
                    user_details_obj.firstname = user_details_form.firstname
                    user_details_obj.lastname = user_details_form.lastname
                    user_details_obj.gender = user_details_form.gender
                    user_details_obj.contact = user_details_form.contact
                    user_details_obj.role = user_details_form.role
                    user_details_obj.blog_url = user_details_form.blog_url
                    user_details_obj.twitter_id = user_details_form.twitter_id
                    user_details_obj.bitbucket_id = user_details_form.topcoder_handle
                    user_details_obj.github_id = user_details_form.github_id
                    user_details_obj.bitbucket_id = user_details_form.bitbucket_id
                    user_details_obj.typing_speed = user_details_form.typing_speed
                    user_details_obj.interest = user_details_form.interest
                    user_details_obj.expertise = user_details_form.expertise
                    user_details_obj.goal = user_details_form.goal
                    # user_details_obj.email = user_details_form.email
                    user_details_obj.save()
                    redirect_url = "/register/profile/" + username + "/"
                    return HttpResponseRedirect(redirect_url)

    except KeyError:
        return error_key(request)


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


# password reset

DEFAULT_FROM_EMAIL = 'amritapurifoss@gmail.com'


class ResetPasswordRequestView(FormView):
    template_name = 'register/forpass.html'
    success_url = '/register/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        '''
        This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        '''
        print email

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False


    def post(self, request, *args, **kwargs):
        """
        A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:  # uses the method written above
            '''
            If the input is an valid email address, then the following code will lookup for users associated with that
            email address. If found then an email will be sent to the address, else an error message will
            be printed on the screen.
            '''
            associated_users = User_info.objects.filter(Q(email=data) | Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'foss@amrita',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    subject_template_name = 'register/password_reset_subject.txt'

                    # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory

                    email_template_name = 'register/password_reset_email.html'

                    # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory

                    subject = loader.render_to_string(subject_template_name, c)

                    # Email subject *must not* contain newlines

                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request,
                                 'An email has been sent to ' + data + ". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            '''
            If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            '''
            associated_users = User_info.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': 'http://foss.amrita.ac.in',  # or your domain
                        'site_name': 'foss@amrita',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    subject_template_name = 'register/password_reset_subject.txt'
                    email_template_name = 'register/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request,
                                 'Email has been sent to ' + data + "'s email address. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = 'register/forpass_reset.html'
    success_url = '/register/login'
    form_class = SetPasswordForm
    is_loggedin = False
    username = ''
    correct_pass = False
    tocken_check = False
    current_pass_error = False

    def get(self, request, *args, **kwargs):
        self.is_loggedin, self.username = get_session_variables(self.request)
        return render(self.request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(PasswordResetConfirmView, self).get_context_data(**kwargs)
        context['is_loggedin'] = self.is_loggedin
        context['username'] = self.username
        return context


    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        self.is_loggedin, self.username = get_session_variables(self.request)

        if self.is_loggedin:

            user = get_object_or_404(User_info, username=self.username)
            form = self.form_class(request.POST)
            if form.is_valid():
                old_password = form.clean_old_password()
                if user.password == hash_func(old_password).hexdigest():
                    self.correct_pass = True
                    self.current_pass_error = True
                    self.success_url = '/register/password_change_success'
        else:
            self.form_class = PasswordResetForm
            form = self.form_class(request.POST)
            assert uidb64 is not None and token is not None  # checked by URLconf
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = UserModel._default_manager.get(pk=uid)
                self.tocken_check = default_token_generator.check_token(user, token)
            except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
                user = None

        if user is not None and (self.tocken_check or self.correct_pass):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has been unsuccessful.')
                return self.form_invalid(form)
        else:
            if not self.current_pass_error:
                messages.error(request, 'The reset password link is no longer valid.')
            else:
                messages.error(request, 'Current password wrong.')
            return self.form_invalid(form)


def password_change_success(request):
    if request.user.is_authenticated():
        is_loggedin = True
        username = request.session['username']
        render_form = False
    else:
        is_loggedin = False
        username = None
        render_form = True

    return render(request, 'register/change_password_success.html', {'is_loggedin':is_loggedin, 'username':username,
                                         'render_form':render_form }, RequestContext(request))

