import os
import urllib
import urllib2
import string

from django.core.mail import send_mail as django_send_mail
from mailer import send_mail as mailer_send_mail

from fossWebsite.settings import ADMINS_EMAIL

from register.models import *
from register.forms import *


def check_captcha(challenge, response, remote_ip):
    """
    Captcha verifcation mechanism
    """
    recaptcha_challenge_field = challenge
    recaptcha_response_field = response
    recaptcha_remote_ip = remote_ip
    recaptcha_url = "http://www.google.com/recaptcha/api/verify"
    recaptcha_private_key = "6LdQssASAAAAAMN5M7BgSjQSXnGRwYJKrtATVXXj"
    recaptcha_data = {
                        'privatekey': recaptcha_private_key,
                        'remoteip': recaptcha_remote_ip,
                        'challenge': recaptcha_challenge_field,
                        'response': recaptcha_response_field,
                    }
    recaptcha_encoded_data = urllib.urlencode(recaptcha_data)
    recaptcha_request = urllib2.Request(recaptcha_url, recaptcha_encoded_data)
    recaptcha_response = urllib2.urlopen(recaptcha_request)
    recaptcha_response_data = str(recaptcha_response.readline())

    recaptcha_response_data = recaptcha_response_data.strip()
    #return recaptcha_response_data
    if recaptcha_response_data == 'true':
        return True
    else:
        return False


def notify_new_user(username, email):
    """
    Notifies the admins regarding a successful user registration
    """
    email_subject = "[FOSS@Amrita][User Registered] " + username
    email_from = "Amritapuri FOSS <amritapurifoss@gmail.com>"
    email_message = """
    A new user has been registered today!
    Username: """ + username + """
    Email: """ + email + """

    --
    Email deamon
    Amritapuri FOSS
    http://amritapurifoss.in
    amritapurifoss@gmail.com
    """

    django_send_mail(email_subject, \
            email_message, \
            email_from, \
            ADMINS_EMAIL, \
            fail_silently = False)


def sendmail_after_userreg(username, password, email_to):
    """
    Email notification to be send to the user
    """
    email_subject = 'FOSS@Amrita User Registration'
    email_from = 'Amritapuri FOSS <amritapurifoss@gmail.com>'
    email_message = """
    You have been successfully registered as a USER at Amritapuri FOSS.
    
    Username: """ + username + """
    Password: """ + password + """
    
    --
    Amritapuri FOSS
    http://amritapurifoss.in
    amritapurifoss@gmail.com
    """    

    django_send_mail(email_subject, \
            email_message, \
            email_from, \
            [email_to], \
            fail_silently = False)

def sendmail_after_pass_change(username, password, email_to):
    """
    Email notification to be send after user password change
    """
    email_subject = 'FOSS@Amrita User Password change'
    email_from = 'Amritapuri FOSS <amritapurifoss@gmail.com>'
    email_message = """
    Your password has been recently changed.
    
    Username: """ + username + """
    New Password: """ + password + """
    
    --
    Amritapuri FOSS
    http://amritapurifoss.in
    amritapurifoss@gmail.com
    """    

    django_send_mail(email_subject, \
            email_message, \
            email_from, \
            [email_to], \
            fail_silently = False)
