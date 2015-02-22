# Django libraries
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Q

from django.core.mail import send_mail as django_send_mail
from mailer import send_mail as mailer_send_mail

# Application specific libraries
from register.views import logged_in
from fossWebsite.helper import get_session_variables
from register.models import User_info
from register.helper import check_captcha
from fossWebsite.settings import ADMINS_EMAIL


def home(request):
    """
    Landing page
    """
    if logged_in(request):
        is_loggedin = True
        username = request.session['username']
    else:
        is_loggedin = False
        username = None

    return render_to_response('home.html', \
            {'is_loggedin':is_loggedin, \
            'username':username}, \
            RequestContext(request))


def search(request):
    """
    Search view
    """
    is_loggedin, username = get_session_variables(request)
    search_field = request.GET['search_field']
    #if search field is empty
    if not search_field:
        return HttpResponseRedirect('/')

    #if search field is not empty
    else:
        result = []
        is_empty = True

        search_list = search_field.split(' ')
        for term in search_list:
            #search in the firstname and lastname of all members.
            rs_obj = User_info.objects \
                    .filter(Q(firstname__icontains=term) | \
                    Q(lastname__icontains=term))
            for result_object in rs_obj:
                if result_object not in result:
                    result.append(result_object)

        #if search result is not empty
        if result:
            is_empty = False

        return render_to_response( \
                'search_result.html', \
                {'is_empty':is_empty, \
                'is_loggedin':is_loggedin, \
                'username':username, \
                'result':result}, \
                RequestContext(request))

def contact(request):
    """
    View implement contact-us.
    """
    if request.method == 'POST':
        sender_name = str(request.POST['sender_name'])
        sender_email = str(request.POST['sender_email'])
        email_message = str(request.POST['mail_text'])
        email_from = "Amritapuri FOSS <amritapurifoss@gmail.com>"
        # if captcha field is not given
        if not (request.POST['recaptcha_challenge_field'] and request.POST['recaptcha_response_field']):
            return render_to_response('home.html',{'captcha_error':'Captcha required'}, RequestContext(request))
        recaptcha_challenge_field = request.POST['recaptcha_challenge_field']
        recaptcha_response_field = request.POST['recaptcha_response_field']
        recaptcha_remote_ip = ""
        captcha_is_correct = check_captcha(recaptcha_challenge_field, \
                            recaptcha_response_field,recaptcha_remote_ip)
        email_subject = "[Contact Us]:"+ sender_name 

        print captcha_is_correct
        #To-Do: Need to enable captcha once the site is hosted with 
        # with a domain name.
        #if captcha_is_correct:
        django_send_mail(email_subject, \
                            email_message, \
                            email_from, \
                            [sender_email, 'amritapurifoss@gmail.com'], \
                            fail_silently= False)
        return render_to_response( 'contact_success.html', \
                {}, RequestContext(request))
        

    return HttpResponseRedirect('/')
