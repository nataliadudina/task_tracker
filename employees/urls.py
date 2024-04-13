from django.urls import path, include
from rest_framework.routers import DefaultRouter

from employees.apps import EmployeesConfig
from employees.views import EmployeeViewSet, BusyEmployeesView

app_name = EmployeesConfig.name

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employees')

urlpatterns = [
    path('', include(router.urls)),
    path('busy-employees/', BusyEmployeesView.as_view(), name='busy_employees'),
]
