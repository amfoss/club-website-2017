from django import forms
from captcha.fields import ReCaptchaField


# Write to us (Contact field)
class ContactForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    message = forms.CharField(max_length=1500)
    captcha = ReCaptchaField()
