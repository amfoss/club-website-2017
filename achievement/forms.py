from django.forms import ModelForm
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.db import models
from achievement.models import *

# Create your models here.
ACHIEVEMENT_CHOICE = (('acm','ACM_ICPC'), ('article','Article'), \
        ('contribution','Contribution'), ('gsoc','GSoC'), \
        ('intern','Internship'), ('speaker','Speaker'), \
        ('contest','Contest'), ('other','Other'))
INTERN_CHOICE = (('internship','Internship'),('masters','Masters'), \
        ('exchange student','Exchange programme'))
SPEAKER_CHOICE =(('talk',' Talk'), ('demo','Demo'), \
        ('workshop','Workshop'), ('paper','Paper Presentation'), \
        ('other','Other'))
LEVEL_CHOICE = (('regional','Regional'), ('finals','World-Finals'))


class AddContributionForm(ModelForm):
    """
    Form to add open source Contribution
    """
    bug_id = forms.IntegerField(
        required=True,
        label='bug_id',
        widget=forms.TextInput(
            attrs={'placeholder':'Bug ID/Ticket'}
        )
    )

    org_name=forms.CharField(
         required=True,
         label='Organization Name',
         widget=forms.TextInput(
            attrs={'placeholder': 'Organization Name'}
         )
    )

    bug_url=forms.URLField(
         required=True,
         label='Bug URL',
         widget=forms.TextInput(
            attrs={'placeholder': 'URL'}
         )
    )

    bug_description=forms.CharField(
         required=True,
         label='Description',
         widget=forms.Textarea(
            attrs={'placeholder': 'Description of Bug', \
            'cols': 20, 'rows': 5}
         )
    )

    class Meta:
	model = Contribution
	exclude = ['username', 'achievement_id',]


class UpdateContributionForm(ModelForm):
    """
    Form to update open source Contribution
    """
    bug_id = forms.IntegerField(
        required=True,
        label='bug_id',
        widget=forms.TextInput(
            attrs={'placeholder':'Bug ID/Ticket'}
        )
    )

    org_name=forms.CharField(
         required=True,
         label='Organization Name',
         widget=forms.TextInput(
            attrs={'placeholder': 'Organization Name'}
         )
    )

    bug_url=forms.URLField(
         required=True,
         label='Bug URL',
         widget=forms.TextInput(
            attrs={'placeholder': 'URL'}
         )
    )

    bug_description=forms.CharField(
         required=True,
         label='Description',
         widget=forms.Textarea(
            attrs={'placeholder': 'Description of Bug', \
            'cols': 20, 'rows': 5}
         )
    )

    class Meta:
	model = Contribution
	exclude = ['username', 'achievement_id',]


class AddArticleForm(ModelForm):
    """
    Form to add information about articles
    """
    title=forms.CharField(
         required=True,
         label='Title',
         widget=forms.TextInput(
            attrs={'placeholder': 'Title of the article'}
         )
    )

    area=forms.CharField(
         required=True,
         label='Area',
         widget=forms.TextInput(
            attrs={'placeholder': 'Area of the article'}
         )
    )

    magazine_name=forms.CharField(
         required=True,
         label='Magazine',
         widget=forms.TextInput(
            attrs={'placeholder': 'Magazine Name'}
         )
    )

    publication_date=forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Published Date (YYYY-MM-DD)'}
        )
    )

    class Meta:
        model = Article
        exclude = ['username', 'achievement_id',]


class UpdateArticleForm(ModelForm):
    """
    Form to update information about articles
    """
    title=forms.CharField(
         required=True,
         label='Title',
         widget=forms.TextInput(
            attrs={'placeholder': 'Title of the article'}
         )
    )

    area=forms.CharField(
         required=True,
         label='Area',
         widget=forms.TextInput(
            attrs={'placeholder': 'Area of the article'}
         )
    )

    magazine_name=forms.CharField(
         required=True,
         label='Magazine',
         widget=forms.TextInput(
            attrs={'placeholder': 'Magazine Name'}
         )
    )

    publication_date=forms.DateField(
        required=True,
        widget=DateTimePicker(
            options={"pickTime": False, 
                "format":"YYYY-MM-DD"},
            attrs={'placeholder': 'Published Date (YYYY-MM-DD)'}
        )
    )

    class Meta:
        model = Article
        exclude = ['username', 'achievement_id',]



class AdddupdateForm(ModelForm):
    """
    Form to add Daily updates
    """    

    daily_updates=forms.CharField(
         required=True,
         label='Description',
         widget=forms.Textarea(
            attrs={'placeholder': 'Daily Updates', \
            'cols': 20, 'rows': 5}
         )
    )

    class Meta:
        model = Dailyupdate
        exclude = ['username', 'achievement_id',]



class UpdatedupdateForm(ModelForm):
    """
    Form to add Daily updates
    """    

    daily_updates=forms.CharField(
         required=True,
         label='Description',
         widget=forms.Textarea(
            attrs={'placeholder': 'Daily Updates', \
            'cols': 20, 'rows': 5}
         )
    )
    

    class Meta:
        model = Dailyupdate
        exclude = ['username', 'achievement_id',]



class AddSpeakerForm(ModelForm):
    """
    Form to add information about Speaker
    """ 

    title=forms.CharField(
         required=True,
         label='Title',
         widget=forms.TextInput(
            attrs={'placeholder': 'Title of the talk'}
         )
    )

    speaker_type=forms.CharField(
         required=True,
         label='Speaker Type',
         widget=forms.Select(
            choices=SPEAKER_CHOICE,
            attrs={'placeholder': 'Speaker Type'}
         )
    )

    conference_name=forms.CharField(
         required=True,
         label='Conference Name',
         widget=forms.TextInput(
            attrs={'placeholder': 'Name of the Conference'}
         )
    )

    speaker_url=forms.URLField(
         required=True,
         label='Speaker URL',
         widget=forms.TextInput(
            attrs={'placeholder': 'Speaker URL'}
         )
    )

    year = forms.IntegerField(
        required=True,
        label='Year',
        widget=forms.TextInput(
            attrs={'placeholder':'Year'}
        )
    )

    class Meta:
        model = Speaker
        exclude = ['username', 'achievement_id',]


class AddGSoCForm(ModelForm):
    """
    Form to add information about GSoC
    """

    project_title=forms.CharField(
         required=True,
         label='Project Title',
         widget=forms.TextInput(
            attrs={'placeholder': 'Title of your GSoC Project'}
         )
    )

    organization=forms.CharField(
         required=True,
         label='Organization',
         widget=forms.TextInput(
            attrs={'placeholder': 'Name of the Organization'}
         )
    )

    mentor_name=forms.CharField(
         required=True,
         label='Mentor Name',
         widget=forms.TextInput(
            attrs={'placeholder': 'Name of your GSoC mentor'}
         )
    )

    gsoc_url=forms.URLField(
         required=True,
         label='GSoC URL',
         widget=forms.TextInput(
            attrs={'placeholder': 'Link to GSoC'}
         )
    )

    class Meta:
        model = Gsoc
        exclude = ['username', 'achievement_id',]



class AddInternForm(ModelForm):
    """
    Form to add information about Internship
    """

    place=forms.CharField(
         required=True,
         label='Organization',
         widget=forms.TextInput(
            attrs={'placeholder': 'Organization'}
         )
    )

    intern_type=forms.CharField(
         required=True,
         label='Internship Type',
         widget=forms.Select(
            choices=INTERN_CHOICE,
            attrs={'placeholder': 'Type of internship'}
         )
    )

    period=forms.CharField(
         required=True,
         label='Period',
         widget=forms.TextInput(
            attrs={'placeholder': 'Duration of internship'}
         )
    )


    class Meta:
        model = Intern
        exclude = ['username', 'achievement_id',]


class UpdateInternForm(ModelForm):
    """
    Form to update information about Internship
    """

    place=forms.CharField(
         required=True,
         label='Organization',
         widget=forms.TextInput(
            attrs={'placeholder': 'Organization'}
         )
    )

    intern_type=forms.CharField(
         required=True,
         label='Internship Type',
         widget=forms.Select(
            choices=INTERN_CHOICE,
            attrs={'placeholder': 'Type of internship'}
         )
    )

    period=forms.CharField(
         required=True,
         label='Period',
         widget=forms.TextInput(
            attrs={'placeholder': 'Duration of internship'}
         )
    )


    class Meta:
        model = Intern
        exclude = ['username', 'achievement_id',]


class AddIcpcForm(ModelForm):
    """
    Form to add ICPC details
    """ 

    team_name=forms.CharField(
         required=True,
         label='Title',
         widget=forms.TextInput(
            attrs={'placeholder': 'Team Name'}
         )
    )
    yr_of_participation = forms.IntegerField(
        required=True,
        label='Year',
        widget=forms.TextInput(
            attrs={'placeholder':'Year (YYYY)'}
        )
    )
    level=forms.CharField(
         required=True,
         label='level',
         widget=forms.Select(
            choices=LEVEL_CHOICE,
            attrs={'placeholder': 'Level'}
         )
    )
    ranking=forms.IntegerField(
         required=True,
         label='Ranking',
         widget=forms.TextInput(
            attrs={'placeholder': 'Ranking'}
         )
    )
    participant1_name=forms.CharField(
         required=True,
         label='participant1_name',
         widget=forms.TextInput(
            attrs={'placeholder': 'Name of 1st Team member'}
         )
    )
    participant2_name=forms.CharField(
         required=True,
         label='participant2_name',
         widget=forms.TextInput(
            attrs={'placeholder': 'Name of 2nd Team member'}
         )
    )
    participant3_name=forms.CharField(
         required=True,
         label='participant3_name',
         widget=forms.TextInput(
            attrs={'placeholder': 'Name of 3rd team member'}
         )
    )
    participant1_email=forms.EmailField(
         required=True,
         label='Email ID',
         widget=forms.TextInput(
            attrs={'placeholder': 'Email ID of 1st Team member'}
         )
    )
    participant2_email=forms.EmailField(
         required=True,
         label='Email ID',
         widget=forms.TextInput(
            attrs={'placeholder': 'Email ID of 2nd Team member'}
         )
    )
    participant3_email=forms.EmailField(
         required=True,
         label='Email ID',
         widget=forms.TextInput(
            attrs={'placeholder': 'Email ID of 3rd team member'}
         )
    )
    class Meta:
        model = ACM_ICPC_detail
        exclude = ['username', 'achievement_id',]


