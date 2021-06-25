from rest_framework import serializers
from .models import (Department, Designation, Employee, EmployeeSlots)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSlots
        fields = '__all__'


