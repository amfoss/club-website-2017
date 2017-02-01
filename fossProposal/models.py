from django.db import models
from register.models import User_info


class Proposal(models.Model):

    title = models.CharField(max_length=300)
    type = models.CharField(max_length=200)

    date = models.DateField(auto_now_add=False)
    duration = models.CharField(max_length=100)

    venue = models.CharField(max_length=200)
    field = models.CharField(max_length=300)

    speakers = models.CharField(max_length=500)

    prerequisites = models.TextField()
    level = models.CharField(max_length=200)
    course_plan = models.TextField()

    expected_no_of_participants = models.IntegerField()

    sponsor_list = models.TextField()

    benefit_for_students = models.TextField()
    innovation = models.TextField()

    lab_requirements = models.CharField(max_length=200)
    icts_support = models.TextField()

    remote_or_local = models.CharField(max_length=200)
    local_travel_details = models.CharField(max_length=200)
    local_accommodation_details = models.CharField(max_length=200)
    local_food = models.CharField(max_length=200)

    estimated_cost = models.FloatField()

    date_added = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User_info, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_field_values(self):
        return [field.value_to_string(self) for field in Proposal._meta.fields]
