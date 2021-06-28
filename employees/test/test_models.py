import random
from datetime import date, datetime, time

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from employees.models import Department, Designation, Employee, EmployeeSlots
from rest_framework.test import APIClient


class BaseTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command(
            "loaddata", "/home/dev/project/kcoverseas/Meetings/group.json", verbosity=0
        )
        cls.employee_code = Employee.objects.values_list("employeecode", flat=True)
        cls.employee_codes = random.sample([x for x in cls.employee_code], k=2)


class EmployeeTestCase(BaseTestClass):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test_user", password="Pa$$w0rd")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_func(self):
        employee = Employee.objects.last()
        self.assertIsInstance(employee, Employee)
        self.assertIsInstance(employee.employeeid, int)
        self.assertIsInstance(employee.firstname, str)
        self.assertIsInstance(employee.middlename, str)
        self.assertIsInstance(employee.lastname, str)
        self.assertIsInstance(employee.employeecode, str)
        self.assertIsInstance(employee.designation, Designation)
        self.assertIsInstance(employee.department, Department)
        self.assertIsInstance(employee.createdon, datetime)
        self.assertIsInstance(employee.modifiedon, datetime)
        self.assertIsNotNone(employee.firstname)
        self.assertEqual(
            str(employee), str(employee.firstname) + " " + str(employee.lastname)
        )


class EmployeeSlotsTestCase(BaseTestClass):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test_user", password="Pa$$w0rd")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_func(self):
        employeeslot = EmployeeSlots.objects.last()
        self.assertIsInstance(employeeslot, EmployeeSlots)
        self.assertIsInstance(employeeslot.employeeslotid, int)
        self.assertIsInstance(employeeslot.employee1, Employee)
        self.assertIsInstance(employeeslot.employee2, Employee)
        self.assertIsInstance(employeeslot.meetingdate, date)
        self.assertIsInstance(employeeslot.meetingfromtime, time)
        self.assertIsInstance(employeeslot.meetingtotime, time)
        self.assertIsInstance(employeeslot.createdon, datetime)
        self.assertEqual(
            str(employeeslot),
            str(employeeslot.employeeslotid) + " " + str(employeeslot.meetingdate),
        )


class DesignationTestCase(BaseTestClass):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test_user", password="Pa$$w0rd")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_func(self):
        designation = Designation.objects.last()
        self.assertIsInstance(designation, Designation)
        self.assertIsInstance(designation.designationid, int)
        self.assertIsInstance(designation.name, str)
        self.assertIsInstance(designation.createdon, datetime)
        self.assertEqual(str(designation), str(designation.name))


class DepartmentTestCase(BaseTestClass):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test_user", password="Pa$$w0rd")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_func(self):
        department = Department.objects.last()
        self.assertIsInstance(department, Department)
        self.assertIsInstance(department.departmentid, int)
        self.assertIsInstance(department.name, str)
        self.assertIsInstance(department.createdon, datetime)
        self.assertEqual(str(department), str(department.name))
