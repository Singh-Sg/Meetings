from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import Http404, JsonResponse
from django.urls import reverse

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import (Department, Designation, Employee, EmployeeSlots)
from employees.forms import EmployeeSlotsForm
from .serializers import *
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


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
        if serializer.is_valid():
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
            raise Http404

    def get(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeesList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeSlotsList(generics.ListCreateAPIView):
    queryset = EmployeeSlots.objects.all()
    serializer_class = EmployeeSlotsSerializer

class EmployeeSlotsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeSlots.objects.all()
    serializer_class = EmployeeSlotsSerializer


@csrf_exempt
def index(request, *args, **kwrgs):
    """
    List all Employees, or create a new Meetings.
    """
    if request.method == 'GET':
        employee = Employee.objects.all()
        employeeslots = EmployeeSlots.objects.all()
        # serializer = EmployeeSerializer(employee, many=True)
        # return Response(serializer.data)
        return render(request, 'employees/index.html', {"context":employee, "employeeslots":employeeslots,})
    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_slots(id):
    from django.db.models import Q
    data = EmployeeSlots.objects.filter(
            Q(employee1_id =id) | 
            Q(employee2_id = id)).values(
            "meetingfromtime","meetingtotime").order_by("meetingfromtime")
    slot_from = []
    slot_to = []
    start_hour = []
    start_minute = []
    end_hour = []
    end_minute = []
    for x in data:
        start_hour.append(x["meetingfromtime"].hour)
        start_minute.append(x["meetingfromtime"].minute)
        end_hour.append(x["meetingtotime"].hour)
        end_minute.append(x["meetingtotime"].minute)
    return {
        "slot_from":{"start_hour":start_hour, "start_minute":start_minute,},
        "slot_to":{"end_hour":end_hour, "end_minute":end_minute,},
    }

@csrf_exempt
def tasks(request, *args, **kwrgs):
    if request.method == 'POST':
        id = request.POST.get('id')
        id2 = request.POST.get('id2')
        if not id or not id2:
            return Response("Id missing", status=status.HTTP_400_BAD_REQUEST)
        emp1_slot = get_slots(int(id))
        emp2_slot = get_slots(int(id2)) 
        available = []
        for x in range(24):
            if not ((x in emp1_slot["slot_from"]["start_hour"]) or (x in emp2_slot["slot_from"]["start_hour"])):
                available += [f"{x}:00:00 - {x+1}:00:00"]
        print(id, id2)
        return JsonResponse({"data":available})


class book_slot(APIView):
    def post(self, request, formate = None, *args, **kwargs):
        id = request.POST.get('emp_id_1')
        id2 = request.POST.get('emp_id_2')
        slot = request.POST.get('slot_select')
        message = request.POST.get('message')
        if not all([slot, id, id2]):
            return Response("Id missing", status=status.HTTP_400_BAD_REQUEST)
        slot  = slot.replace(' ', '').split('-')
        start_slot = datetime.strptime(slot[0], '%H:%M:%S').time()
        end_slot = datetime.strptime(slot[1], '%H:%M:%S').time()
        data = [{
            "employee1": id, # get_object_or_404(Employee, pk=id),
            "employee2" : id2, # get_object_or_404(Employee, pk=id2),
            "meetingdate":datetime.now().date(),
            "meetingfromtime":start_slot,
            "meetingtotime":end_slot,
            "message": message,
        }]
        serializer = EmployeeSlotsSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            messages.success(request,('Booked'))
            return HttpResponseRedirect(reverse('index'))
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
