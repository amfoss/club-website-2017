from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from register.models import User_info
# Create your models
STATUS_CHOICES=(('o','Ongoing'),('c','Completed'))

class Project(models.Model):
	project_id = models.BigIntegerField(primary_key=True, blank=False, unique=True, validators=[MinLengthValidator(0),MaxLengthValidator(100)])
	project_name = models.CharField(max_length=100, blank=False)
	project_description = models.CharField(max_length=200)
	project_duration = models.CharField(max_length=50)

class Project_mentor(models.Model):
	project_id = models.ForeignKey(Project, blank=False, null=False)
	username = models.ForeignKey(User_info, blank=False, null=False)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)

class Project_student(models.Model):
	project_id = models.ForeignKey(Project, blank=False, null=False)
	username = models.ForeignKey(User_info, blank=False, null=False)


