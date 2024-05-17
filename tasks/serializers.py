from rest_framework import serializers

from employees.models import Employee
from . import validators
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """ Сериализатор задачи"""
    assigned_employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), allow_null=True)

    class Meta:
        model = Task
        fields = '__all__'

    def validate(self, data):
        # Валидация поля deadline
        deadline = data.get('deadline')

        # Проверка установки дедлайна
        if deadline:
            deadline_validator = validators.TaskDeadlineValidator()
            deadline_validator(deadline)

        # Валидация поля parent_task
        parent_task = data.get('parent_task')
        instance = self.instance

        if parent_task:
            parent_task_validator = validators.TaskParentTaskValidator()
            parent_task_validator(parent_task, instance)

        return data


class ImportantTaskSerializer(serializers.Serializer):
    """ Сериализатор важных задач - неназначенных задач, от которых есть зависимые задачи уже в работе """

    id = serializers.IntegerField(source='pk')
    task = serializers.CharField(source='name')   # определяется поле 'task', которое будет содержать имя задачи
    deadline = serializers.DateField()

    class Meta:
        fields = ['id', 'task', 'deadline', 'employee']

    def to_representation(self, instance):
        # Добавление информации о назначенном сотруднике
        representation = super().to_representation(instance)  # получение базовой сериализации объекта.
        from employees.serializers import SimpleEmployeeSerializer  # локальный импорт
        # сериализация объекта Employee, связанного с задачей.
        representation['employee'] = SimpleEmployeeSerializer(instance.assigned_employee).data
        return representation
