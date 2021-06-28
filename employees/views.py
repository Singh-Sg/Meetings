from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from employees.utils import is_slot_available
from django.template.loader import render_to_string
from django.http import HttpResponse

from .models import Employee, EmployeeSlots
from .serializers import *
from django.conf import settings


class EmployeesList(APIView):
    """
    List all employee, or create a new employee.
    """

    def get(self, request, format=None):
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetail(APIView):
    """
    Retrieve, update or delete a employee instance.
    """

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk, format=None):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeSlotsList(generics.ListCreateAPIView):
    """
    API list view of employee slots
    """

    queryset = EmployeeSlots.objects.all()
    serializer_class = EmployeeSlotsSerializer


class EmployeeSlotsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Slot list, retrieve, update
    """

    queryset = EmployeeSlots.objects.all()
    serializer_class = EmployeeSlotsSerializer


class IndexAPI(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


def index(request, *args, **kwrgs):
    """
    List all Employees, or create a new Meetings.
    """
    if request.method == "GET":
        employee = Employee.objects.all()
        paginator = Paginator(employee, settings.PAGINATED_BY)
        page_number = request.GET.get("page")
        employees = paginator.get_page(page_number)
        return render(
            request,
            "employees/index.html",
        )


class AvailableSlot(APIView):
    """
    Getting employees details to create neeting by checking available slots.
    """

    def get(self, request, *args, **kwrgs):
        emp_id_1 = request.GET.get("emp_id_1")
        emp_id_2 = request.GET.get("emp_id_2")
        meeting_date = request.GET.get("meeting_date")
        if not meeting_date:
            return Response(
                {"message": "Please provide meeting_date"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (not emp_id_1) or (not emp_id_2):
            return Response(
                {"message": "Two employee code must be supplied"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if emp_id_1 == emp_id_2:
            return Response(
                {"message": "Both Employeed code must be different"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        meeting_date = datetime.strptime(meeting_date, "%Y-%m-%d")
        available_slot = is_slot_available(emp_id_1, emp_id_2, meeting_date)
        return Response({"available_slot": available_slot}, status=status.HTTP_200_OK)


class BookSlot(APIView):
    """
    Saving meetings
    """

    def post(self, request):
        serializer = EmployeeSlotsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "Meeting has been scheduled successfully"},
                status=status.HTTP_201_CREATED,
            )
