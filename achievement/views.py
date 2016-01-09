# Django libraries
from django.shortcuts import HttpResponseRedirect, render
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext


# Application specific functions
from achievement.models import *
from achievement.forms import *
from fossWebsite.helper import error_key, csrf_failure, logged_in
from fossWebsite.helper import get_session_variables
from achievement.helper import get_achievement_id


# Create your views here.
def email_registered(email):
    user = User_info.objects.filter(email = email)
    return bool(user)

def get_username_from_email(email):
    if(email_registered):
        user = User_info.objects.filter(email=email)
        if user:
            return user[0].username
    else:
        return ''

def achieve_viewall(request):
    """
    View to display recent 5 achievements
    """
    is_loggedin, username = get_session_variables(request)
    contrib_list = []
    article_list = []
    gsoc_list = []
    speaker_list = []
    intern_list = []
    contest_participant_list = []
    icpc_participants_regional_list = []
    icpc_participants_final_list = []
    dupdates_list = []

    contrib_list_all = Contribution.objects.all()
    contrib_list = Contribution.objects.all()[:5]
    dupdates_list = Dailyupdate.objects.all()[:5]
    article_list = Article.objects.all()[:5]
    gsoc_list = Gsoc.objects.all()[:5]
    speaker_list = Speaker.objects.all()[:5]
    intern_list = Intern.objects.all()[:5]
    contest_list = Contest_won.objects.all()[:5]

    
    contrib_org = {}
    if contrib_list_all:
        for contrib in contrib_list_all:
            if contrib.org_name not in contrib_org.keys():
                contrib_org[contrib.org_name] = 0

        for contrib in contrib_list_all:
            contrib_org[contrib.org_name] += 1

    if contest_list:	
        contest_participant_list = []
	for contest_won_obj in contest_list:	
	    c_id = contest_won_obj.contest_id
	    c_p_objs = Contest_won_participant.objects.filter(contest_id = c_id)
	    contest_participant_list.extend(c_p_objs)
    
    icpc_list_regionals = ACM_ICPC_detail.objects.filter(level='regional').order_by('ranking')[:2]
    if icpc_list_regionals:
        for icpc_obj in icpc_list_regionals:
            team = icpc_obj.team_name
            member1 = [icpc_obj.participant1_name, \
                get_username_from_email(icpc_obj.participant1_email)]

            member2 = [icpc_obj.participant2_name, \
                get_username_from_email(icpc_obj.participant2_email)]

            member3 = [icpc_obj.participant3_name, \
                get_username_from_email(icpc_obj.participant3_email)]

            icpc_participant_list = [icpc_obj, member1,member2,member3]
            icpc_participants_regional_list.append(icpc_participant_list)

    icpc_list_finals = ACM_ICPC_detail.objects.filter(level='finals').order_by('ranking')[:2]
    if icpc_list_finals:
        for icpc_obj in icpc_list_finals:
            team = icpc_obj.team_name
            member1 = [icpc_obj.participant1_name, \
                get_username_from_email(icpc_obj.participant1_email)]

            member2 = [icpc_obj.participant2_name, \
                get_username_from_email(icpc_obj.participant2_email)]

            member3 = [icpc_obj.participant3_name, \
                get_username_from_email(icpc_obj.participant3_email)]

            icpc_participant_list = [icpc_obj, member1,member2,member3]
            icpc_participants_final_list.append(icpc_participant_list)

    return render_to_response('achievement/achievement_viewall.html',\
		{'username':username, \
                'is_loggedin':is_loggedin, \
                'contrib_list':contrib_list, \
		'dupdates_list':dupdates_list, \
                'contrib_org':contrib_org,\
                'article_list':article_list, \
                'gsoc_list':gsoc_list, \
                'speaker_list':speaker_list, \
                'intern_list':intern_list, \
                'contest_list':contest_list, \
                'contest_participant_list':contest_participant_list, \
                'icpc_participants_final_list':icpc_participants_final_list, \
                'icpc_participants_regional_list':icpc_participants_regional_list}, \
                RequestContext(request))

def contrib_viewall(request):
    """
    View to display all contributions
    """
    is_loggedin, username = get_session_variables(request)
    contrib_list = Contribution.objects.all()
    contrib_org = {}
    if contrib_list:
        for contrib in contrib_list:
            if contrib.org_name not in contrib_org.keys():
                contrib_org[contrib.org_name] = 0

        for contrib in contrib_list:
            contrib_org[contrib.org_name] += 1
    
    if contrib_list:
        return render_to_response('achievement/contrib_viewall.html', \
                {'is_loggedin':logged_in(request), \
                'username':username, \
                'contrib_list':contrib_list, 'contrib_org':contrib_org}, \
                RequestContext(request))
    else:
        return render_to_response('achievement/noview.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'type': 'Contribution'}, \
                RequestContext(request))

def article_viewall(request):
    """
    View to display all articles published
    """
    is_loggedin, username = get_session_variables(request)
    article_list = Article.objects.all()

    if article_list:
        return render_to_response('achievement/article_viewall.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'article_list':article_list}, \
                RequestContext(request))
    else:
        return render_to_response('achievement/noview.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'type': 'Article'}, \
                RequestContext(request))


def dupdates_viewall(request):
    """
    View to display all Dailyupdates
    """
    is_loggedin, username = get_session_variables(request)
    dupdates_list = Dailyupdate.objects.all()

    if dupdates_list:
        return render_to_response('achievement/dupdate_viewall.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'dupdates_list':dupdates_list}, \
                RequestContext(request))
    else:
        return render_to_response('achievement/noview.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'type': 'Dailyupdate'}, \
                RequestContext(request))



def gsoc_viewall(request):
    """
    View to display all GSOCers
    """
    is_loggedin, username = get_session_variables(request)
    gsoc_list = Gsoc.objects.all()

    if gsoc_list:
        return render_to_response('achievement/gsoc_viewall.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'gsoc_list':gsoc_list}, \
                RequestContext(request))
    else:
        return render_to_response('achievement/noview.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'type': 'Gsoc'}, \
                RequestContext(request))


def speaker_viewall(request):
    """
    View to display all Speakers
    """
    is_loggedin, username = get_session_variables(request)
    speaker_list = Speaker.objects.all()

    if speaker_list:
        return render_to_response('achievement/speaker_viewall.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'speaker_list':speaker_list}, \
                RequestContext(request))
    else:
        return render_to_response('achievement/noview.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'type': 'Speaker'}, \
                RequestContext(request))

def intern_viewall(request):
    """
    View to display all internships done
    """
    is_loggedin, username = get_session_variables(request)
    intern_list = Intern.objects.all()

    if intern_list:
        return render_to_response('achievement/intern_viewall.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'intern_list':intern_list}, \
                RequestContext(request))
    else:
        return render_to_response('achievement/noview.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'type': 'Internship'}, \
                RequestContext(request))

def contest_won_viewall(request):
    """
    View to display all Contest Won
    """
    is_loggedin, username = get_session_variables(request)
    contest_list = Contest_won.objects.all()

    if contest_list:	
        contest_participant_list = []
        for contest_won_obj in contest_list:	
            c_id = contest_won_obj.contest_id
            c_p_objs = Contest_won_participant.objects. \
                    filter(contest_id = c_id)
            contest_participant_list.extend(c_p_objs)

        return render_to_response('achievement/contest_viewall.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'contest_list':contest_list, \
                'contest_participant_list':contest_participant_list}, \
                RequestContext(request))
    else:
        return render_to_response('achievement/noview.html', \
                {'is_loggedin':is_loggedin, \
                'username':username, \
                'type': 'Contest\'s won'}, \
                RequestContext(request))

def icpc_viewall(request):
    """
    View to display all ICPCers.
    """
    is_loggedin, username = get_session_variables(request)
    icpc_participants_list = []
    p_list= []
    icpc_list = ACM_ICPC_detail.objects.all().order_by('ranking')
    if icpc_list:

        for icpc_obj in icpc_list:
            
            team = icpc_obj.team_name
            member1 = [icpc_obj.participant1_name, \
                get_username_from_email(icpc_obj.participant1_email)]

            member2 = [icpc_obj.participant2_name, \
                get_username_from_email(icpc_obj.participant2_email)]

            member3 = [icpc_obj.participant3_name, \
                get_username_from_email(icpc_obj.participant3_email)]

            icpc_participant_list = [icpc_obj, member1,member2,member3]
            icpc_participants_list.append(icpc_participant_list)
            
        return render_to_response('achievement/icpc_viewall.html', \
            {'is_loggedin':logged_in(request), \
            'username':username, \
            'icpc_list':icpc_list,\
            'icpc_participants_list':icpc_participants_list}, RequestContext(request))

    else:
        return render_to_response('achievement/noview.html', \
                {'is_loggedin':logged_in(request), \
                'username':username, \
                'type': 'ACM ICPC Contest'}, \
                RequestContext(request))


def insert_contribution(request):
    """
    View to add new Contribution.
    Models used: Achievement, Contribution
    """
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')

        # User is logged in
        else:
            if request.method == 'POST':
                form = AddContributionForm(request.POST)

                # Invalid form imput
                if not form.is_valid():
                    error = "Invalid inputs"
                    return render_to_response('achievement/new_contribution.html', \
                            {'form': form, \
                            'error':error, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))

                # Form is valid
                else:
                    # Get the new achievement_id
                    achievement_id = get_achievement_id(request)	
                    achievement_type = "contribution"

                    # Saving inputs
                    achievement_obj = Achievement(achievement_id, \
                            achievement_type, \
                            username)
                    achievement_obj.save()
                    contribution_obj = form.save(commit = False)
                    contribution_obj.achievement_id = achievement_obj
                    contribution_obj.achieve_typ = achievement_type
                    user_obj = get_object_or_404(User_info, username = username)
                    contribution_obj.username = user_obj
                    contribution_obj.save()
                    return render_to_response('achievement/success.html', \
                            {'achievement_type':achievement_type, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))
            # Method is not POST
            else:
                    return render_to_response('achievement/new_contribution.html', \
                            {'form': AddContributionForm, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))
    except KeyError:
        return error_key(request)


def insert_article(request):
    """
    View to add new Article.
    Models used: Achievement, Article
    """
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')

        # User is logged in
        else:
            if request.method == 'POST':
                form = AddArticleForm(request.POST)

                # Invalid form imput
                if not form.is_valid():
                    error = "Invalid inputs"
                    return render_to_response('achievement/new_article.html', \
                            {'form':form, \
                            'error':error, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))

                # Form is valid
                else:
                    # Get the new achievement_id
                    achievement_id = get_achievement_id(request)	
                    achievement_type = "Article"

                    # Saving inputs
                    achievement_obj = Achievement(achievement_id, \
                            achievement_type, \
                            username)
                    achievement_obj.save()
                    contribution_obj = form.save(commit = False)
                    contribution_obj.achievement_id = achievement_obj
                    contribution_obj.achieve_typ = achievement_type
                    user_obj = get_object_or_404(User_info, username = username)
                    contribution_obj.username = user_obj
                    contribution_obj.save()
                    return render_to_response('achievement/success.html', \
                            {'achievement_type':achievement_type, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))
            # Method is not POST
            else:
                return render_to_response('achievement/new_article.html', \
                        {'form': AddArticleForm, \
                        'is_loggedin':is_loggedin, \
                        'username':username}, \
                        RequestContext(request))
    except KeyError:
        return error_key(request)


def insert_dupdates(request):
    """
    View to add new Update.
    Models used: Achievement, Dailyupdate
    """
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')

        # User is logged in
        else:
            if request.method == 'POST':
                form = AdddupdateForm(request.POST)

                # Invalid form imput
                if not form.is_valid():
                    error = "Invalid inputs"
                    return render_to_response('achievement/new_dupdate.html', \
                            {'form':form, \
                            'error':error, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))

		# Form is valid
                else:
                    # Get the new achievement_id
                    achievement_id = get_achievement_id(request)	
                    achievement_type = "Dailyupdate"

                    # Saving inputs
                    achievement_obj = Achievement(achievement_id, \
                            achievement_type, \
                            username)
                    achievement_obj.save()
                    contribution_obj = form.save(commit = False)
                    contribution_obj.achievement_id = achievement_obj
                    contribution_obj.achieve_typ = achievement_type
                    user_obj = get_object_or_404(User_info, username = username)
                    contribution_obj.username = user_obj
                    contribution_obj.save()
                    return render_to_response('achievement/success.html', \
                            {'achievement_type':achievement_type, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))
            # Method is not POST
            else:
                return render_to_response('achievement/new_dupdate.html', \
                        {'form': AdddupdateForm, \
                        'is_loggedin':is_loggedin, \
                        'username':username}, \
                        RequestContext(request))
    except KeyError:
        return error_key(request)


def insert_talk(request):
    """
    View to add new talk
    Models used: Achievement, Speaker
    """
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')

        # User is logged in
        else:
            if request.method == 'POST':
                form = AddSpeakerForm(request.POST)

                # Invalid form imput
                if not form.is_valid():
                    error = "Invalid inputs"
                    return render_to_response('achievement/new_speaker.html', \
                            {'form':form, \
                            'error':error, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))

                # Form is valid
                else:
                    # Get the new achievement_id
                    achievement_id = get_achievement_id(request)	
                    achievement_type = "Speaker"

                    # Saving inputs
                    achievement_obj = Achievement(achievement_id, \
                            achievement_type, \
                            username)
                    achievement_obj.save()
                    contribution_obj = form.save(commit = False)
                    contribution_obj.achievement_id = achievement_obj
                    contribution_obj.achieve_typ = achievement_type
                    user_obj = get_object_or_404(User_info, username = username)
                    contribution_obj.username = user_obj
                    contribution_obj.save()
                    return render_to_response('achievement/success.html', \
                            {'achievement_type':achievement_type, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))
            # Method is not POST
            else:
                return render_to_response('achievement/new_speaker.html', \
                        {'form': AddSpeakerForm, \
                        'is_loggedin':is_loggedin, \
                        'username':username}, \
                        RequestContext(request))
    except KeyError:
        return error_key(request)


def insert_gsoc(request):
    """
    View to add gsoc details
    Models used: Achievement, GSoC
    """
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')

        # User is logged in
        else:
            if request.method == 'POST':
                form = AddGSoCForm(request.POST)

                # Invalid form imput
                if not form.is_valid():
                    error = "Invalid inputs"
                    return render_to_response('achievement/new_gsoc.html', \
                            {'form':form, \
                            'error':error, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))

                # Form is valid
                else:
                    # Get the new achievement_id
                    achievement_id = get_achievement_id(request)	
                    achievement_type = "GSoC"

                    # Saving inputs
                    achievement_obj = Achievement(achievement_id, \
                            achievement_type, \
                            username)
                    achievement_obj.save()
                    contribution_obj = form.save(commit = False)
                    contribution_obj.achievement_id = achievement_obj
                    contribution_obj.achieve_typ = achievement_type
                    user_obj = get_object_or_404(User_info, username = username)
                    contribution_obj.username = user_obj
                    contribution_obj.save()
                    return render_to_response('achievement/success.html', \
                            {'achievement_type':achievement_type, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))
            # Method is not POST
            else:
                return render_to_response('achievement/new_gsoc.html', \
                        {'form': AddGSoCForm, \
                        'is_loggedin':is_loggedin, \
                        'username':username}, \
                        RequestContext(request))
    except KeyError:
        return error_key(request)


def insert_intern(request):
    """
    View to add internship details
    Models used: Achievement, Intern
    """
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')

        # User is logged in
        else:
            if request.method == 'POST':
                form = AddInternForm(request.POST)

                # Invalid form imput
                if not form.is_valid():
                    error = "Invalid inputs"
                    return render_to_response('achievement/new_intern.html', \
                            {'form':form, \
                            'error':error, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))

                # Form is valid
                else:
                    # Get the new achievement_id
                    achievement_id = get_achievement_id(request)	
                    achievement_type = "Intern"

                    # Saving inputs
                    achievement_obj = Achievement(achievement_id, \
                            achievement_type, \
                            username)
                    achievement_obj.save()
                    contribution_obj = form.save(commit = False)
                    contribution_obj.achievement_id = achievement_obj
                    contribution_obj.achieve_typ = achievement_type
                    user_obj = get_object_or_404(User_info, username = username)
                    contribution_obj.username = user_obj
                    contribution_obj.save()
                    return render_to_response('achievement/success.html', \
                            {'achievement_type':achievement_type, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))
            # Method is not POST
            else:
                return render_to_response('achievement/new_intern.html', \
                        {'form': AddInternForm, \
                        'is_loggedin':is_loggedin, \
                        'username':username}, \
                        RequestContext(request))
    except KeyError:
        return error_key(request)


def insert_icpc(request):
    """
    View to add ICPC details.
    Models used: Achievement, ACM_ICPC_detail
    """
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')

        # User is logged in
        else:
            if request.method == 'POST':
                form = AddIcpcForm(request.POST)

                # Invalid form imput
                if not form.is_valid():
                    error = "Invalid inputs/ Information already exists "
                    return render_to_response('achievement/new_icpc.html', \
                            {'form': form, \
                            'error':error, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))

                # Form is valid
                else:
                    # Get the new achievement_id
                    achievement_id = get_achievement_id(request)    
                    achievement_type = "acm"

                    # Saving inputs
                    achievement_obj = Achievement(achievement_id, \
                            achievement_type, \
                            username)
                    achievement_obj.save()
                    icpc_obj = form.save(commit = False)
                    icpc_obj.achievement_id = achievement_obj
                    user_obj = get_object_or_404(User_info, username = username)
                    icpc_obj.username = user_obj
                    icpc_obj.save()
                    return render_to_response('achievement/success.html', \
                            {'achievement_type':achievement_type, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))
            # Method is not POST
            else:
                    return render_to_response('achievement/new_icpc.html', \
                            {'form': AddIcpcForm, \
                            'is_loggedin':is_loggedin, \
                            'username':username}, \
                            RequestContext(request))
    except KeyError:
        return error_key(request)


def update_contribution(request,achievement_id):
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')
        else:
            #achievement_id = get_object_or_404(Achievement, username = user_name)
            contribution = get_object_or_404(Contribution, achievement_id = achievement_id)
            init_contribution = contribution.__dict__

                #If method is not POST 
            if request.method != 'POST':
                #return form with old details
                return render_to_response('achievement/update_contrib.html',\
                    {'form':UpdateContributionForm(init_contribution),\
                    'is_loggedin':is_loggedin, 'username':username},\
                    RequestContext(request))

            # If method is POST
            else:
                contribution_update_form = UpdateContributionForm(request.POST)
                # Form is not valid
                if not contribution_update_form.is_valid():
                    #return form with old details
                    return render_to_response('achievement/update_contrib.html',\
                        {'form':UpdateContributionForm(init_contribution),\
                        'is_loggedin':is_loggedin, 'username':username},\
                        RequestContext(request)) 
                # Form is valid:
                else:
                    contribution_update = contribution_update_form.save(commit = False)
                    update_contribution_obj = get_object_or_404(Contribution, username = username)
                    update_contribution_obj.bug_id = contribution_update.bug_id
                    update_contribution_obj.org_name = contribution_update.org_name
                    update_contribution_obj.bug_url = contribution_update.bug_url
                    update_contribution_obj.bug_description = contribution_update.bug_description
                    update_contribution_obj.save()  
                    return render_to_response('achievement/success.html', \
                        {'achievement_type':'Update Contribution', \
                        'is_loggedin':is_loggedin, \
                        'username':username}, \
                        RequestContext(request))

    except KeyError:
        return error_key(request)



def update_article(request,achievement_id):
    """
    View to update the artciel information
    """
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')
        else:
            
            article = get_object_or_404(Article, achievement_id = achievement_id)
            init_article = article.__dict__

            #If method is not POST 
            if request.method != 'POST':
                #return form with old details
                return render_to_response('achievement/update_article.html',\
                    {'form':UpdateArticleForm(init_article),\
                    'is_loggedin':is_loggedin, 'username':username},\
                    RequestContext(request))

            # If method is POST
            else:
                article_update_form = UpdateArticleForm(request.POST)
                # Form is not valid
                if not article_update_form.is_valid():
                    #return form with old details
                    return render_to_response('achievement/update_article.html',\
                        {'form':UpdateArticleForm(init_article),\
                        'is_loggedin':is_loggedin, 'username':username},\
                        RequestContext(request)) 
                # Form is valid:
                else:
                    article_update = article_update_form.save(commit = False)
                    update_article_obj = get_object_or_404(Article, username = username)
                    update_article_obj.area = article_update.area
                    update_article_obj.magazine_name = article_update.magazine_name
                    update_article_obj.title = article_update.title
                    update_article_obj.publication_date = article_update.publication_date
                    update_article_obj.save()  
                    return render_to_response('achievement/success.html', \
                        {'achievement_type':'Update Article', \
                        'is_loggedin':is_loggedin, \
                        'username':username}, \
                        RequestContext(request))

    except KeyError:
        return error_key(request)


def update_dupdates(request,achievement_id):
    """
    View to update the updates information
    """
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')
        else:
            
            dupdates = get_object_or_404(Dailyupdate, achievement_id = achievement_id)
            init_dupdates = dupdates.__dict__

            #If method is not POST 
            if request.method != 'POST':
                #return form with old details
                return render_to_response('achievement/update_dupdate.html',\
                    {'form':UpdatedupdateForm(init_dupdates),\
                    'is_loggedin':is_loggedin, 'username':username},\
                    RequestContext(request))

            # If method is POST
            else:
                dupdates_update_form = UpdatedupdateForm(request.POST)
                # Form is not valid
                if not dupdates_update_form.is_valid():
                    #return form with old details
                    return render_to_response('achievement/update_dupdate.html',\
                        {'form':UpdatedupdateForm(init_dupdates),\
                        'is_loggedin':is_loggedin, 'username':username},\
                        RequestContext(request)) 
                # Form is valid:
		else:
                    dupdates_update = dupdates_update_form.save(commit = False)
                    update_dupdates_obj = get_object_or_404(Dailyupdate, username = username)                                        
                    update_dupdates_obj.today_date = dupdates_update.today_date
		    update_dupdates_obj.daily_updates = dupdates_update.daily_updates
                    update_dupdates_obj.save()  
                    return render_to_response('achievement/success.html', \
                        {'achievement_type':'Dailyupdate', \
                        'is_loggedin':is_loggedin, \
                        'username':username}, \
                        RequestContext(request))

    except KeyError:
        return error_key(request)


def update_intern(request,achievement_id):
    """
    View to update the artciel information
    """
    try:
        is_loggedin, username = get_session_variables(request)
        # User is not logged in
        if not logged_in(request):
            return HttpResponseRedirect('/register/login')
        else:
            
            internship = get_object_or_404(Intern, achievement_id = achievement_id)
            init_internship = internship.__dict__

            #If method is not POST 
            if request.method != 'POST':
                #return form with old details
                return render_to_response('achievement/update_intern.html',\
                    {'form':UpdateInternForm(init_internship),\
                    'is_loggedin':is_loggedin, 'username':username},\
                    RequestContext(request))

            # If method is POST
            else:
                intern_update_form = UpdateInternForm(request.POST)
                # Form is not valid
                if not intern_update_form.is_valid():
                    #return form with old details
                    return render_to_response('achievement/update_intern.html',\
                        {'form':UpdateInternForm(init_internship),\
                        'is_loggedin':is_loggedin, 'username':username},\
                        RequestContext(request)) 
                # Form is valid:
                else:
                    intern_update = intern_update_form.save(commit = False)
                    intern_article_obj = get_object_or_404(Intern, username = username)
                    intern_article_obj.place = intern_update.place
                    intern_article_obj.intern_type = intern_update.intern_type
                    intern_article_obj.period = intern_update.period
                    intern_article_obj.save()  
                    return render_to_response('achievement/success.html', \
                        {'achievement_type':'Update Internship', \
                        'is_loggedin':is_loggedin, \
                        'username':username}, \
                        RequestContext(request))

    except KeyError:
        return error_key(request)
