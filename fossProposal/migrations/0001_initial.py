# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('type', models.CharField(max_length=200)),
                ('speakers', models.CharField(max_length=500)),
                ('date', models.DateField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('duration', models.CharField(max_length=100)),
                ('course_plan', models.TextField()),
                ('prerequisites', models.TextField()),
                ('expected_no_of_participants', models.IntegerField()),
                ('sponsor_list', models.TextField()),
                ('benefit_for_student', models.TextField()),
                ('innovation', models.TextField()),
            ],
        ),
    ]
