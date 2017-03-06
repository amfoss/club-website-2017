from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.forms import ModelForm
from django import forms
from django.forms.utils import flatatt
import re


from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.html import format_html_join, format_html
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe

from register.models import User_info

# password reset
from django.utils.translation import ugettext, ugettext_lazy as _


GENDER_CHOICES = (('M', 'Male'), \
        ('F', 'Female'))
ROLE_CHOICES = (('S', 'Student'), \
        ('M', 'Mentor'), \
        ('B', 'Both'))
GOAL_CHOICES = (('startup', 'startup'), \
        ('higher_studies', 'Higher Studies'), \
        ('job', 'Job'), ('other', 'Others'))


#custom functions
def check_alpha(name):
    """
    Checks for the only presence of alphabets
    """
    if re.match("^[a-za-z ]*$",name):
        return True
    else:
        return False


def user_exists(email_):
    """
    Checks if a user exists or not
    """
    if User_info.objects.all().filter(email=email_):
        return True
    else:
        return False


class LoginForm(forms.Form):
    """
    Login form
    """
    username=forms.CharField(
        required=True,
        max_length=100,
        label='Username', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Username'}
        )
    )

    password=forms.CharField(
        required=True,
        max_length=100,
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        )
    )

    def clean_repass(self):
        password = self.cleaned_data['password']
        re_password = self.cleaned_data['repass']
        if password == re_password:
            return password
        else:
            raise forms.ValidationError("Passwords don't match")


class NewRegisterForm(ModelForm):
    """
    Registration form
    """
    firstname=forms.CharField(
         required=True,
         label='First Name', 
         widget=forms.TextInput(
            attrs={'placeholder': 'Firstname'}
         )
    )

    lastname=forms.CharField(
         required=True,
         label='Last Name', 
         widget=forms.TextInput(
            attrs={'placeholder': 'Lastname'}
         )
    )

    gender=forms.CharField(
        required=True,
        label='Gender', 
        widget=forms.Select(
            choices=GENDER_CHOICES, 
            attrs={'placeholder': 'Gender'}
            )
    )

    contact = forms.IntegerField(
        required=True,
        label='Phone number', 
        widget=forms.TextInput(
            attrs={'placeholder':'Phone Number'}
        )
    )

    role=forms.CharField(
        required=True,
        label='Role', 
        widget=forms.Select(
            choices=ROLE_CHOICES, 
            attrs={'placeholder': 'Role'}, 
        )
    )
    blog_url=forms.CharField(
        required=False,
        label='blog_url', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Blog URL'}, 
        )
    )
    twitter_id=forms.CharField(
        required=False,
        label='Twitter ID', 
        widget=forms.TextInput( 
            attrs={'placeholder': 'Twitter ID'}, 
        )
    )
    topcoder_handle=forms.CharField(
        required=False,
        label='Role', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Topcoder Handle'}, 
        )
    )
    github_id=forms.CharField(
        required=False,
        label='Github ID', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Github ID'}, 
        )
    )   
    bitbucket_id=forms.CharField(
        required=False,
        label='Bitbucket ID', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Bitbucket ID'}, 
        )
    )   
    typing_speed=forms.CharField(
        required=True,
        label='Typing Speed', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Typing Speed'}, 
        )
    )
    interest = forms.CharField(
        required=True,
        label='Interests', 
        widget=forms.TextInput(
            attrs={'placeholder':'Interests'}
        )
    )
    expertise = forms.CharField(
        required=True,
        label='Expertise', 
        widget=forms.TextInput(
            attrs={'placeholder':'Expertize'}
        )
    )

    goal=forms.CharField(
        required=True,
        label='Goal', 
        widget=forms.Select(
            choices=GOAL_CHOICES, 
            attrs={'placeholder': 'Goal'}, 
        )
    )
    
    email=forms.EmailField(
        required=True,
        label='Email', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Email Address'}
        )
    )

    username=forms.CharField(
        required=True,
        label='Username', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Username'}
        )
    )

    password=forms.CharField(
        required=True,
        max_length=100,
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        )
    )

    repass = forms.CharField(
        max_length=100,
        required=True,
        label='Re-enter password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Re Enter Your Password'}
        ),
    )


    class Meta:
        model = User_info
	fields = '__all__'

    def clean_name(self):
        """
        Checks for non-alphabets in the username.
        Raises an error if found
        """
        username = self.cleaned_data['username']
        if check_alpha(username):
            return username
        else:
            raise forms.ValidationError("Please enter only alphabets")

    def clean_repass(self):
        """
        If passwords doesn't match, both the password
        fields will be cleard by raising an error
        """
        password = self.cleaned_data['password']
        re_password = self.cleaned_data['repass']
        if password == re_password:
            return password
        else:
            raise forms.ValidationError("Passwords don't match")


class UpdateProfileForm(ModelForm):
    """
    Update Profile Form
    """
    firstname=forms.CharField(
         required=True,
         label='First Name', 
         widget=forms.TextInput(
            attrs={'placeholder': 'Firstname'}
         )
    )

    lastname=forms.CharField(
         required=True,
         label='Last Name', 
         widget=forms.TextInput(
            attrs={'placeholder': 'Lastname'}
         )
    )

    gender=forms.CharField(
        required=True,
        label='Gender', 
        widget=forms.Select(
            choices=GENDER_CHOICES, 
            attrs={'placeholder': 'Gender'}
            )
    )

    contact = forms.IntegerField(
        required=True,
        label='Phone number', 
        widget=forms.TextInput(
            attrs={'placeholder':'Phone Number'}
        )
    )

    role=forms.CharField(
        required=True,
        label='Role', 
        widget=forms.Select(
            choices=ROLE_CHOICES, 
            attrs={'placeholder': 'Role'}, 
        )
    )
    blog_url=forms.CharField(
        required=False,
        label='blog_url', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Blog URL'}, 
        )
    )
    twitter_id=forms.CharField(
        required=False,
        label='Twitter ID', 
        widget=forms.TextInput( 
            attrs={'placeholder': 'Twitter ID'}, 
        )
    )
    topcoder_handle=forms.CharField(
        required=False,
        label='Role', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Topcoder Handle'}, 
        )
    )
    github_id=forms.CharField(
        required=False,
        label='Github ID', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Github ID'}, 
        )
    )   
    bitbucket_id=forms.CharField(
        required=False,
        label='Bitbucket ID', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Bitbucket ID'}, 
        )
    )   
    typing_speed=forms.CharField(
        required=True,
        label='Typing Speed', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Typing Speed'}, 
        )
    )
    interest = forms.CharField(
        required=True,
        label='Interests', 
        widget=forms.TextInput(
            attrs={'placeholder':'Interests'}
        )
    )
    expertise = forms.CharField(
        required=True,
        label='Expertise', 
        widget=forms.TextInput(
            attrs={'placeholder':'Expertize'}
        )
    )

    goal=forms.CharField(
        required=True,
        label='Goal', 
        widget=forms.Select(
            choices=GOAL_CHOICES, 
            attrs={'placeholder': 'Goal'}, 
        )
    )
    """
    email=forms.EmailField(
        required=False,
        label='Email', 
        widget=forms.TextInput(
            attrs={'placeholder': 'Email Address'}
        )
    )"""

    class Meta:
        model = User_info
        exclude = ['password','username','email',]


class ChangePasswordForm(forms.Form):
    """
    Password changer form
    """
    old_password=forms.CharField(
        required=True,
        max_length=100,
        label='Current Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Current Password'}
        )
    )

    new_password = forms.CharField(
        required=True,
        max_length=100,
        label='New Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'New Password'} 
        )
    )

    confirm_new_password = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm new password'} 
        )
    )

    def clean_repass(self):
        """
        If passwords doesn't match, both the password
        fields will be cleard by raising an error
        """
        password = self.cleaned_data['new_password']
        re_password = self.cleaned_data['confirm_new_password']
        if password == re_password:
            return password
        else:
            raise forms.ValidationError("Passwords don't match")



# custom password reset


class ReadOnlyPasswordHashWidget(forms.Widget):
    def render(self, name, value, attrs):
        encoded = value
        final_attrs = self.build_attrs(attrs)

        if not encoded or encoded.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary = mark_safe("<strong>%s</strong>" % ugettext("No password set."))
        else:
            try:
                hasher = identify_hasher(encoded)
            except ValueError:
                summary = mark_safe("<strong>%s</strong>" % ugettext(
                    "Invalid password format or unknown hashing algorithm."))
            else:
                summary = format_html_join('',
                                           "<strong>{0}</strong>: {1} ",
                                           ((ugettext(key), value)
                                            for key, value in hasher.safe_summary(encoded).items())
                                           )

        return format_html("<div{0}>{1}</div>", flatatt(final_attrs), summary)


class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super(ReadOnlyPasswordHashField, self).__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial

    def has_changed(self, initial, data):
        return False


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User_info
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }

            self.send_mail(subject_template_name, email_template_name,
                           context, from_email, user.email,
                           html_email_template_name=html_email_template_name)


# password reset

from django import forms

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)
