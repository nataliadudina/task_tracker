from rest_framework import serializers

from tasks.models import Task
from tasks.serializers import TaskSerializer
from .models import Employee
from . import validators


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate(self, data):
        # Валидация поля experience
        experience_validator = validators.ExperienceValidator()
        experience = data.get('experience')
        if experience is not None:
            experience_validator(experience)

        # Валидация полей first_name, middle_name, last_name
        name_validator = validators.NameValidator()
        for field in ['first_name', 'middle_name', 'last_name']:
            name = data.get(field)
            if name is not None:
                name_validator(name)

        return data


class SimpleEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['fullname']


class BusyEmployeeSerializer(serializers.ModelSerializer):
    """ Сериализатор для представления данных о занятых сотрудниках. """
    active_tasks_count = serializers.IntegerField()
    current_tasks = serializers.SerializerMethodField()

    def get_current_tasks(self, employee):
        """
        Получает список текущих активных задач сотрудника.

        Args:
            employee: Сотрудник, для которого нужно получить задачи.
        Returns:
            Список сериализованных данных о текущих активных задачах сотрудника.
        """
        # Получаем активные задачи сотрудника со статусом 'in_progress'
        tasks = Task.objects.filter(assigned_employee=employee, status='in_progress')
        # Сериализуем данные о задачах
        return TaskSerializer(tasks, many=True).data

    class Meta:
        model = Employee
        fields = ['id', 'fullname', 'active_tasks_count', 'current_tasks']
