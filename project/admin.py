from django.contrib import admin
from project.models import Project, Project_mentor, Project_student
# Register your models here.
admin.site.register(Project)
admin.site.register(Project_mentor)
admin.site.register(Project_student)
