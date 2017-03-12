# Django libraries
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q

from django.core.mail import send_mail as django_send_mail

# Application specific libraries


from register.models import User_info
from .forms import ContactForm


def home(request):
    """
    Landing page
    """
    form = ContactForm()
    if request.user.is_authenticated():
        is_loggedin = True
        username = request.user.username
        render_form = False
    else:
        is_loggedin = False
        username = None
        render_form = True

    return render(request, 'home.html', {'is_loggedin':is_loggedin, 'username':username, 'form':form,
                                         'render_form':render_form }, RequestContext(request))


def search(request):
    """
    Search view
    """
    if request.user.is_authenticated():
        is_loggedin = True
        username = request.user.username
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

        return render(request, \
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
    if request.user.is_authenticated():
        is_loggedin = True
        username = request.user.username
    else:
        is_loggedin = False
        username = None
    if request.POST:
        form = ContactForm(request.POST)

        # Validate the form: the captcha field will automatically
        # check the input
        if form.is_valid():
            sender_name = str(form.cleaned_data['name'])
            sender_email = str(form.cleaned_data['email'])
            email_message = str(form.cleaned_data['message'])
            email_from = "Amritapuri FOSS <amritapurifoss@gmail.com>"
            email_subject = "[Contact Us]:" + sender_name

            django_send_mail(email_subject, email_message, email_from, [sender_email, 'amritapurifoss@gmail.com'],
                             fail_silently=False)

            return render(request, 'contact_success.html', {}, RequestContext(request))

        else:



            captcha_error = "Error in Captcha, Please try again"

            return render(request, 'home.html', {'is_loggedin': is_loggedin, 'username': username, 'form': form,
                                                 'captcha_error':captcha_error }, RequestContext(request))



