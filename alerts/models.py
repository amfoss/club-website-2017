from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
# Create your models here.

ALERT_CHOICES = (('i','Internships'),('t','TechFest'),('c','Contest'),('o','Others'))

class Alert_info(models.Model):
	alert_id =  models.IntegerField(primary_key=True, blank=False, unique=True, validators=[MinLengthValidator(0),MaxLengthValidator(100)])
	alert_url = models.URLField(max_length=200, blank=False, null=False)
	alert_type = models.CharField(max_length=1, choices=ALERT_CHOICES, blank=False, null=False)	
	alert_description = models.CharField(max_length=200)
