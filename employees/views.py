from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from employees.models import Employee
from employees.paginators import EmployeePaginator
from employees.serializers import EmployeeSerializer, BusyEmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
        Представление для выполнения операций CRUD (Create, Read, Update, Delete) с сотрудниками.

        serializer_class: Сериализатор, определяющий формат данных при взаимодействии с сотрудниками через API.
        queryset: Запрос к базе данных для получения всех сотрудников.
        pagination_class: Класс пагинации для разбиения списка сотрудников на страницы при выводе на клиенте.
        """
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    pagination_class = EmployeePaginator


class BusyEmployeesView(APIView):
    """ Представление для получения списка занятых сотрудников и их активных задач. """

    def get(self, request):
        # Получение список занятых сотрудников и подсчёт количества их активных задач
        busy_employees = Employee.objects.annotate(
            active_tasks_count=Count('tasks', filter=Q(tasks__status='in_progress'))).order_by('-active_tasks_count')
        # Сериализация данных о занятых сотрудниках
        serializer = BusyEmployeeSerializer(busy_employees, many=True)
        return Response(serializer.data)
