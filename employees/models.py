from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='First Name')
    middle_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Middle Name')
    last_name = models.CharField(max_length=255, verbose_name='Last Name')
    position = models.CharField(max_length=255, verbose_name='Position')
    experience = models.PositiveSmallIntegerField(verbose_name='Experience')  # years
    tasks_completed = models.PositiveSmallIntegerField(verbose_name='Tasks Completed')  # number of completed tasks

    @property
    def fullname(self):
        """
        Возвращает полное имя сотрудника.
        Если у сотрудника есть отчество, будет возвращены фамилия и инициалы.
        """
        if self.middle_name:
            return f"{self.last_name} {self.first_name[0]}. {self.middle_name[0]}."
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return f"{self.fullname} - {self.position}"

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
