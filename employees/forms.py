from django import forms
from employees.models import EmployeeSlots


class EmployeeSlotsForm(forms.ModelForm):
    class Meta:
        model = EmployeeSlots
        fields = "__all__"
