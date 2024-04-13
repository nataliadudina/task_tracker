from django.db import models

from employees.models import Employee


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    description = models.TextField(null=True, blank=True, verbose_name='Description')

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ]
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, verbose_name='Priority')
    deadline = models.DateField(verbose_name='Deadline')

    STATUS_CHOICES = [
        ('to_assign', 'To assign'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, verbose_name='Status')
    completion_time = models.DateField(null=True, blank=True, verbose_name='Completion Time')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='linked_task', verbose_name='Parent Task')
    assigned_employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL,
                                          related_name='tasks')

    def __str__(self):
        return f'{self.name} - {self.status}'

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
