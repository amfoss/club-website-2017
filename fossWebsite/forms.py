from django import forms
from captcha.fields import CaptchaField


# Write to us (Contact field)
class CaptchaTestForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    message = forms.Textarea()
    captcha = CaptchaField()
