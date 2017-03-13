from django import forms
from captcha.fields import ReCaptchaField
from django.contrib.auth import get_user_model
from registration.forms import RegistrationForm


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    message = forms.CharField(max_length=1500)
    captcha = ReCaptchaField()


class CustomRegisterUserForm(RegistrationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.TextInput(
            attrs={'placeholder': 'Email Address'}
        )
    )

    username = forms.CharField(
        required=True,
        label='Username',
        widget=forms.TextInput(
            attrs={'placeholder': 'Username'}
        )
    )

    password1 = forms.CharField(
        required=True,
        max_length=100,
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        )
    )

    password2 = forms.CharField(
        max_length=100,
        required=True,
        label='Re-enter password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Re Enter Your Password'}
        ),
    )