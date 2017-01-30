from django.db import models

# Create your models here.


class Proposal(models.Model):
    title = models.CharField(max_length=300)
    type = models.CharField(max_length=200)
    speakers = models.CharField(max_length=500)

    date = models.DateField(auto_now_add=False)
    date_added = models.DateField(auto_now_add=True)
    duration = models.CharField(max_length=100)

    course_plan = models.TextField()
    prerequisites = models.TextField()

    expected_no_of_participants = models.IntegerField()

    sponsor_list = models.TextField()

    benefit_for_student = models.TextField()

    innovation = models.TextField()

    def __str__(self):
        return self.title
