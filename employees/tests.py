from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task
from .models import Employee


class EmployeeTestCase(APITestCase):
    """ Тестирование приложения 'сотрудник' """

    def setUp(self) -> None:
        self.first_employee = Employee.objects.create(first_name="John", middle_name="Albert", last_name="Smith",
                                                      position="Developer", experience=5, tasks_completed=18)
        self.second_employee = Employee.objects.create(first_name="Jane", middle_name="Elizabeth", last_name="Doe",
                                                       position="Designer", experience=3, tasks_completed=10)

    def test_create_employee(self):
        """ Тестирование создания сотрудника"""
        data = {
            "first_name": "John",
            "middle_name": "Albert",
            "last_name": "Smith",
            "position": "Developer",
            "experience": 5,
            "tasks_completed": 18
        }
        response = self.client.post('/employees/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.all().exists())

    def test_list_employees(self):
        """ Тестирование вывода списка сотрудников"""

        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['first_name'], 'John')

    def test_read_employee(self):
        """ Тестирование просмотра сотрудника"""

        response = self.client.get('/employees/', kwargs={'pk': self.first_employee.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['first_name'], 'John')
        self.assertEqual(response.data['results'][0]['last_name'], 'Smith')

    def test_update_employee(self):
        """ Тестирование обновление сотрудника"""

        updated_data = {
            'experience': 5
        }
        response = self.client.patch(reverse('employees:employees-detail', kwargs={'pk': self.first_employee.id}),
                                     data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['experience'], updated_data['experience'])

    def test_delete_employee(self):
        """ Тестирование удаление сотрудника"""

        response = self.client.delete(reverse('employees:employees-detail', kwargs={'pk': self.first_employee.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(id=self.first_employee.id)

    def test_validate_name(self):
        """ Тестирование валидации имени сотрудника"""

        updated_data = {
            'first_name': 'Charles1'
        }
        response = self.client.patch(reverse('employees:employees-detail', kwargs={'pk': self.first_employee.id}),
                                     data=updated_data)

        self.assertIn("Names must contain only letters and hyphens.", response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BusyEmployeesTestCase(APITestCase):
    """ Тестирование представления BusyEmployeesView """

    def setUp(self) -> None:
        # Создание сотрудников
        self.employee1 = Employee.objects.create(first_name="John", last_name="Doe", position="Developer", experience=5)
        self.employee2 = Employee.objects.create(first_name="Jane", last_name="Smith", position="Designer",
                                                 experience=11)
        self.employee3 = Employee.objects.create(first_name="Alice", last_name="Johnson", position="Manager",
                                                 experience=7)

        # Создание задач для каждого сотрудника
        Task.objects.create(name="Develop Login Page", assigned_employee=self.employee1, deadline="2024-08-10",
                            priority="medium", status='in_progress')
        Task.objects.create(name="Test User Authentication", assigned_employee=self.employee2, deadline="2024-09-07",
                            priority="high", status='in_progress')
        Task.objects.create(name="Create API Endpoints", assigned_employee=self.employee1, deadline="2024-07-12",
                            priority="medium", status='in_progress')

    def test_busy_employees_view(self):
        """ Тестирование вывода списка сотрудников и их задач в порядке загруженности """

        response = self.client.get(reverse('employees:busy_employees'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что список содержит правильное количество элементов
        self.assertEqual(len(response.data), 3)

        # Проверка, что сотрудник с наибольшим количеством активных задач идет первым
        self.assertEqual(response.data[0]['fullname'], 'Doe John')
        self.assertEqual(response.data[0]['active_tasks_count'], 2)

        # Проверка, что сотрудник с наименьшим количеством активных задач идет последним
        self.assertEqual(response.data[-1]['fullname'], 'Johnson Alice')
        self.assertEqual(response.data[-1]['active_tasks_count'], 0)
