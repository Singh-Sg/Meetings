from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from employees import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('employees-list/', views.EmployeesList.as_view()),
    path('employees-edit/<int:pk>/', views.EmployeeDetail.as_view()),
    path('employeesslot-list/', views.EmployeeSlotsList.as_view()),
    path('employeesslotdetail-list/', views.EmployeeSlotsDetail.as_view()),
    path('book_slot/', views.book_slot.as_view(), name = "bookslot"),
]

urlpatterns = format_suffix_patterns(urlpatterns)