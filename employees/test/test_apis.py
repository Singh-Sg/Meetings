import json
import random
from datetime import date, time

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from employees.models import Employee
from rest_framework.test import APIClient


class BaseTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command(
            "loaddata", "/home/dev/project/kcoverseas/Meetings/group.json", verbosity=0
        )
        cls.employee_code = Employee.objects.values_list("employeecode", flat=True)
        cls.employee_codes = random.sample([x for x in cls.employee_code], k=2)


class AvailableSlotAPITestCase(BaseTestClass):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test_user", password="Pa$$w0rd")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_available_slot_api(self):
        data = {
            "emp_id_1": self.employee_codes[0],
            "emp_id_2": self.employee_codes[1],
            "meeting_date": date.today(),
        }
        response = self.client.get(reverse("tasks"), data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.content).get("available_slot"), list)

    def test_available_slot_without_code(self):
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content).get("message"),
            "Please provide meeting_date",
        )
    def test_available_slot_same_code(self):
        data = {
            "emp_id_1": self.employee_codes[0],
            "emp_id_2": self.employee_codes[0],
            "meeting_date": date.today(),
        }
        response = self.client.get(reverse("tasks"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content).get("message"),
            "Both Employeed code must be different",
        )


class BookSlotAPITestCase(BaseTestClass):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test_user", password="Pa$$w0rd")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.data = {
            "emp_id_1": self.employee_codes[0],
            "emp_id_2": self.employee_codes[1],
            "meeting_date": date.today().replace(day=26),
        }
        response = self.client.get(reverse("tasks"), self.data)
        self.available_slots = json.loads(response.content).get("available_slot")
        for x in range(24):
            self.random_slot = f"{time().replace(hour=x,)} - {time().replace(hour=x+1) if x != 23 else time().replace(hour=0)}"
            if self.random_slot not in self.available_slots:
                break

    def test_book_slot_empty_body(self):
        response = self.client.post(reverse("bookslot"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content).get("emp_id_1")[0], "This field is required."
        )
        self.assertEqual(
            json.loads(response.content).get("emp_id_2")[0], "This field is required."
        )
        self.assertEqual(
            json.loads(response.content).get("slot_select")[0],
            "This field is required.",
        )

    def test_book_slot_without_slot(self):
        data = self.data
        response = self.client.post(reverse("bookslot"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content).get("slot_select")[0],
            "This field is required.",
        )

    def test_book_slot_with_slot(self):
        data = self.data
        data["slot_select"] = random.choice(self.available_slots)
        response = self.client.post(reverse("bookslot"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.content).get("message"),
            "Meeting has been scheduled successfully",
        )

    def test_book_slot_not_avail(self):
        data = self.data
        data["slot_select"] = self.random_slot
        response = self.client.post(reverse("bookslot"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
           [*json.loads(response.content).values()][0][0], "Slot is not available"
        )

    def test_book_slot_duration(self):
        data = self.data
        slot = self.random_slot
        slot = slot[:3] + str(random.choice(range(10, 59))) + slot[5:]
        data["slot_select"] = slot
        response = self.client.post(reverse("bookslot"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            [*json.loads(response.content).values()][0][0],
            "Slot duration must be 1 hour",
        )

    def test_book_slot_sequence(self):
        data = self.data
        for x in range(23):
            random_slot = f"{time().replace(hour=x+1)} - {time().replace(hour=x) if x != 23 else time().replace(hour=0)}"
            if random_slot not in self.available_slots:
                break
        data["slot_select"] = random_slot
        response = self.client.post(reverse("bookslot"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            [*json.loads(response.content).values()][0][0],
            "End time must be later then start time",
        )

    def test_book_slot_format(self):
        data = self.data
        for x in range(10, 22):
            random_slot = f"{time().replace(hour=x)} - {time().replace(hour=x-1) if x != 23 else time().replace(hour=0)}"
            if random_slot not in self.available_slots:
                break
        data["slot_select"] = "random_slot"
        response = self.client.post(reverse("bookslot"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            [*json.loads(response.content).values()][0][0], "Invalid slot format"
        )
