from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):

   class Meta:
      model = Employee 
      fields = ('service_number', 'name', 'surname', 'department', 'is_curator', 'is_admin','telegram_id', 'hire_date', 'telegram_registration_date')