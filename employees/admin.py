from django.contrib import admin
from django.db.models.base import Model

# Register your models here.
from .models import *


class EmployeeSlotsAdmin(admin.ModelAdmin):
    """
    EmployeeSlots Admin view
    """
    model = EmployeeSlots
    list_display = (
        "employee1",
        "employee2",
        "meetingdate",
        "meetingfromtime",
        "meetingtotime",
        "message",
    )
    search_fields = (
        "employee1__firstname",
        "employee2__firstname",
        "employee2__lasttname",
        "employee1__lasttname",
    )
    # list_filter =(
    #     "meetingfromtime",
    #     "meetingtotime",
    #     "meetingdate"
    # )


admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee)
admin.site.register(EmployeeSlots, EmployeeSlotsAdmin)
