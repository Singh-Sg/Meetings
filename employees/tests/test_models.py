from django.test import TestCase
from employees.models import (
Department,
Designation,
Employee,
EmployeeSlots,
)
from datetime import datetime

class DepartmentTestCase(TestCase):
    def setUp(self):
        Department.objects.create(name='Engineering Department', createdon = datetime.now())

    def test_department(self):
        name = Department.objects.get(name='Engineering Department')
        createdon = Department.objects.get(createdon=datetime.datetime(2021, 6, 22, 23, 35, 49, 725343))

# class Designation(models.Model):
#     designationid = models.AutoField(db_column='DesignationId', primary_key=True)
#     name= models.CharField(max_length=100, blank=False, null=False, db_column='Name')
#     createdon= models.DateTimeField(auto_now_add=True, db_column='CreatedOn')

#     def __str__(self):
#         return str(self.name)
#     def __unicode__(self):
#         return str(self.name)


# class Employee(models.Model):
#     employeeid= models.AutoField(db_column='EmployeeId', primary_key=True)
#     firstname= models.CharField(max_length=100, blank=False, null=False, db_column='FirstName')
#     middlename=models.CharField(max_length=100, blank=False, null=False, db_column='MiddleName')
#     lastname=models.CharField(max_length=100, blank=False, null=False, db_column='LastName')
#     employeecode=models.CharField(max_length=30, blank=False, null=False, db_column='EmployeeCode')
#     designation=models.ForeignKey(Designation, on_delete=models.DO_NOTHING, blank=False, null=False, db_column='DesignationId')
#     department= models.ForeignKey(Department,on_delete=models.DO_NOTHING, blank=False, null=False, db_column='DepartmentId')
#     createdon= models.DateTimeField(auto_now_add=True, db_column='CreatedOn')
#     modifiedon=models.DateTimeField(auto_now=True, db_column='ModifiedOn')
#     def __str__(self):
#         return str(self.firstname)+' '+str(self.lastname)
#     def __unicode__(self):
#         return str(self.firstname)+' '+str(self.lastname)


# class EmployeeSlots(models.Model):
#     employeeslotid= models.AutoField(db_column='EmployeeSlotId', primary_key=True)
#     employee1= models.ForeignKey(Employee, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='EmployeeId1')
#     employee2=models.ForeignKey(Employee, related_name='employeeslot',on_delete=models.DO_NOTHING, blank=True, null=True,db_column='EmployeeId2')
#     meetingdate=models.DateField(blank=True, null=True, db_column='MeetingDate')
#     meetingfromtime=models.TimeField(blank=True, null=True,db_column='MeetingFromTime')
#     meetingtotime=models.TimeField(blank=True, null=True,db_column='MeetingToTime')
#     message= models.TextField(blank=True, null=True)
#     createdon= models.DateTimeField(auto_now_add=True, db_column='CreatedOn')
        
#     def __str__(self):
#         return str(self.employeeslotid)+' '+str(self.meetingdate)

