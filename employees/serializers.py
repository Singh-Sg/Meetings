from rest_framework import serializers
from .models import Employee, EmployeeSlots
from datetime import datetime, date
from django.shortcuts import get_object_or_404
from employees.utils import is_slot_available


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    designation_name = serializers.CharField(source='designation.name', read_only=True)

    class Meta:
        model = Employee
        fields = ("employeecode", "firstname", "middlename", "lastname",  "department_name", "designation_name")


class EmployeeSlotsSerializer(serializers.Serializer):

    emp_id_1 = serializers.CharField()
    emp_id_2 = serializers.CharField()
    slot_select = serializers.CharField()
    message = serializers.CharField(allow_null=True, required=False)
    meeting_date = serializers.DateField(allow_null=True, required=False)

    def validate(self, data):
        id = data.get("emp_id_1")
        id2 = data.get("emp_id_2")
        meeting_date = data.get("meeting_date")
        slot = data.get("slot_select")
        message = data.get("message")
        if not all([slot, id, id2]):
            raise serializers.ValidationError("Slot, Id and Id2 must not be empty")
        try:
            slot = slot.replace(" ", "").split("-")
            start_slot = datetime.strptime(slot[0], "%H:%M:%S").time()
            end_slot = datetime.strptime(slot[1], "%H:%M:%S").time()
        except:
            raise serializers.ValidationError("Invalid slot format")
        avail_slot = is_slot_available(id, id2, meeting_date)
        if (end_slot.hour == 0) and (start_slot.hour == 23):
            if (end_slot.minute == 0) and (start_slot.minute == 0):
                duration = 3600
            else:
                raise serializers.ValidationError("Slot duration must be 1 hour")
        else:
            duration = datetime.combine(date.today(), end_slot) - datetime.combine(
                date.today(), start_slot
            )
            duration = duration.total_seconds()
        if duration < 0:
            raise serializers.ValidationError("End time must be later then start time")
        elif duration != 3600:
            raise serializers.ValidationError("Slot duration must be 1 hour")
        slot = f"{str(start_slot)} - {str(end_slot)}"
        if slot not in avail_slot:
            raise serializers.ValidationError("Slot is not available")
        data = {
            "employee1": get_object_or_404(Employee, employeecode=id),
            "employee2": get_object_or_404(Employee, employeecode=id2),
            "meetingdate": meeting_date,
            "meetingfromtime": start_slot,
            "meetingtotime": end_slot,
            "message": message,
        }
        return data

    def create(self, validated_data):
        slot = EmployeeSlots.objects.create(**validated_data)
        return slot
