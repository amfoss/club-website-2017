from django.db import models
from django.urls import reverse

from register.models import User_info


class Attendance(models.Model):

    # student details
    username = models.ForeignKey(User_info, related_name='student', on_delete=models.CASCADE)

    # date and time added
    date_added = models.DateTimeField(auto_now_add=True)

    # added by
    added_by = models.ForeignKey(User_info, related_name='attendance_taker', on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('attendance-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username
