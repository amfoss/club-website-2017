from rest_framework import serializers

from attendance.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('username', 'date_added', 'present', 'added_by')
