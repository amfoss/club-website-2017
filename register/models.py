from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models
from django.utils import six
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
ROLE_CHOICES = (('S', 'Student'), ('M', 'Mentor'), ('B', 'Both'))
GOAL_CHOICES = (('startup', 'startup'), ('higher_studies', 'Higher Studies'), ('job', 'Job'), ('other', 'Others'))


class User_info(AbstractUser):

    firstname = models.CharField(max_length=20, blank=True, null=True, unique=False)
    lastname = models.CharField(max_length=20, blank=True, null=True, unique=False)
    gender = models.CharField(max_length=1, blank=True, null=True, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=1, blank=True, null=True, choices=ROLE_CHOICES)
    blog_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_id = models.CharField(max_length=30, blank=True, null=True)
    topcoder_handle = models.CharField(max_length=30, blank=True, null=True)
    github_id = models.CharField(max_length=30, blank=True, null=True)
    bitbucket_id = models.CharField(max_length=30, blank=True, null=True)
    typing_speed = models.BigIntegerField(blank=True, null=True)
    interest = models.CharField(max_length=200, blank=True, null=True)
    expertise = models.CharField(max_length=200, blank=True, null=True)
    goal = models.CharField(max_length=15, choices=GOAL_CHOICES, blank=True, null=True)

    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        primary_key=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    class Meta:
        db_table = 'User_info'

    def get_absolute_url(self):
        return reverse('proposal-detail', kwargs={'pk': self.pk})


class Student(models.Model):
    username = models.ForeignKey(User_info, related_name='user_student', on_delete=models.CASCADE)

    # college
    roll_number = models.CharField(max_length=200, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    cgpa = models.CharField(max_length=10, blank=True, null=True)

    # lab
    mentors = models.CharField(max_length=200, blank=True, null=True)
    system_number = models.CharField(max_length=10, blank=True, null=True)

    # responsibilities

    responsibility1 = models.CharField(max_length=600, blank=True, null=True)
    responsibility2 = models.CharField(max_length=600, blank=True, null=True)
    responsibility3 = models.CharField(max_length=600, blank=True, null=True)
    responsibility4 = models.CharField(max_length=600, blank=True, null=True)
    responsibility5 = models.CharField(max_length=600, blank=True, null=True)
    responsibility_count = models.CharField(max_length=10, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.username.firstname + ' ' + self.username.lastname

    def __str__(self):
        return self.username.username + ' ' + self.username.lastname


