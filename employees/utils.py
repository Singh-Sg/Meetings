from django.db.models import Q
from employees.models import EmployeeSlots
from datetime import datetime, date, time


def get_slots(employee_code, meeting_date):

    """
    Finding slots
    """
    data = EmployeeSlots.objects.filter(
        Q(
            Q(employee1__employeecode=employee_code)
            | Q(employee2__employeecode=employee_code)
        )
        & Q(meetingdate=meeting_date)
    ).values("meetingfromtime", "meetingtotime")
    start_hour = []
    end_hour = []
    for x in data:
        start_hour.append(x["meetingfromtime"].hour)
        end_hour.append(x["meetingtotime"].hour)
    return {
        "start_hour": start_hour,
        "end_hour": end_hour,
    }


def is_slot_available(id, id2, meeting_date):
    """
    Fining available slot
    """
    emp1_slot = get_slots(id, meeting_date)
    emp2_slot = get_slots(id2, meeting_date)
    available_slots = []
    for x in range(24):
        if not ((x in emp1_slot["start_hour"]) or (x in emp2_slot["start_hour"])):
            available_slots += [
                f"{time().replace(hour=x)} - {time().replace(hour=x+1) if x != 23 else time().replace(hour=0)}"
            ]
    return available_slots
