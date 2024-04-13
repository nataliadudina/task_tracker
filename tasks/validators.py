from django.utils import timezone
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from employees.models import Employee


class TaskDeadlineValidator:
    """ Проверка, что срок выполнения задачи не в прошлом и не слишком далеко в будущем """
    def __call__(self, value):
        # Определение текущей даты и времени
        now = timezone.now().date()

        # Определение максимального срока выполнения задачи (например, 30 дней в будущем)
        max_deadline = now + timedelta(days=30)

        # Проверка срока
        if value <= now:
            raise ValidationError(
                _('Deadline cannot be in the past.'),
                code='deadline_in_past',
            )
        elif value > max_deadline:
            raise ValidationError(
                _('Deadline cannot be more than 30 days in the future.'),
                code='deadline_too_far_in_future',
            )


class TaskParentTaskValidator:
    """ Проверка, что родительская задача не ссылается на саму себя """

    def __call__(self, value, instance):
        if value == instance:
            raise ValidationError(
                _('A task cannot be its own parent.'),
                code='parent_task_self_reference',
            )


class TaskAssignedEmployeeValidator:
    """ Проверка, что назначенный на задачу сотрудник существует """

    def __call__(self, value):
        if value is not None:
            if Employee.objects.filter(pk=value.pk).exists():
                return value.id
            else:
                raise ValidationError(
                    _('The assigned employee does not exist.'),
                    code='assigned_employee_does_not_exist',
                )
