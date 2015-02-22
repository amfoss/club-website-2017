from django.db import models

# Create your models here.
EVENT_CHOICE = (('scholarship','Scholarship'),('workshop','Workshop'),('internship','Internship'),('conference','Conference'),('contest','Contest'),('techfest','Tech-Fest'),('others','Others'))

class Event(models.Model):
        event_id = models.BigIntegerField( primary_key=True, blank=False, unique=True)
        name = models.CharField(max_length=50, blank=False, null=False)
        description = models.CharField(max_length=200)
        event_type = models.CharField(max_length=15, choices=EVENT_CHOICE)
        deadline = models.DateField()
        event_url = models.URLField(max_length=200)

