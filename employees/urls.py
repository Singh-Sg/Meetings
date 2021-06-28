from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static

from employees import views

from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.AvailableSlot.as_view(), name='tasks'),
    path('employees-list/', views.EmployeesList.as_view()),
    path('employees-edit/<int:pk>/', views.EmployeeDetail.as_view()),
    path('employeesslot-list/', views.EmployeeSlotsList.as_view()),
    path('employeesslotdetail-list/', views.EmployeeSlotsDetail.as_view()),
    path('book_slot/', views.BookSlot.as_view(), name = "bookslot"),
    path('index_api/', views.IndexAPI.as_view(), name = "index_api"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
