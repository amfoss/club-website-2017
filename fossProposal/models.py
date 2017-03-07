from django.db import models
from django.urls import reverse

from register.models import User_info


class Proposal(models.Model):

    # basic information
    title = models.CharField(max_length=300)
    type = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=False)
    duration = models.CharField(max_length=100)
    venue = models.CharField(max_length=200)
    topic = models.CharField(max_length=300)
    speakers = models.CharField(max_length=500)
    nat_or_inter = models.CharField(max_length=500)
    trainer_bio = models.TextField(blank=True, null=True)
    coordinators = models.CharField(max_length=400)
    level = models.CharField(max_length=200)
    expected_no_of_participants = models.CharField(max_length=200)

    # prerequisites
    prerequisites_software = models.TextField(blank=True, null=True)
    prerequisites_hardware = models.TextField(blank=True, null=True)
    prerequisites_knowledge = models.TextField(blank=True, null=True)

    # course
    course_plan = models.TextField(blank=True, null=True)
    student_short_list = models.TextField(blank=True, null=True)

    # financial
    travel = models.CharField(max_length=200, blank=True, null=True)
    trainer_fee = models.CharField(max_length=200, blank=True, null=True)
    accommodation = models.CharField(max_length=200, blank=True, null=True)
    transportation = models.CharField(max_length=200, blank=True, null=True)
    other = models.CharField(max_length=200, blank=True, null=True)

    # lab requirements
    lab_requirements = models.CharField(max_length=200)
    icts_support = models.TextField(blank=True, null=True)

    # permissions
    permisions = models.TextField()

    # other
    other_info = models.TextField(blank=True, null=True)

    date_added = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User_info, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('proposal-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
