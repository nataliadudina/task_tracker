import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from tasks.models import Task


class TasksTestCase(APITestCase):
    """ Тестирование приложения 'задачи' """

    def setUp(self) -> None:
        # Создание сотрудника
        self.employee = Employee.objects.create(first_name="John", last_name="Doe", position="Developer", experience=5)

        # Создание задач
        self.first_task = Task.objects.create(name="Develop Login Page", assigned_employee=self.employee,
                                              deadline="2024-08-10", priority="medium", status='in_progress')
        self.second_task = Task.objects.create(name="Test User Authentication", deadline="2024-09-07", priority="high",
                                               status='to_assign')
        self.third_task = Task.objects.create(name="Create API Endpoints", assigned_employee=self.employee,
                                              deadline="2024-07-12", priority="medium", status='in_progress')

    def test_create_task(self):
        """ Тестирование создания задачи """
        data = {
            "name": "Create a magic button",
            "priority": "low",
            "status": "in_progress",
            "deadline": "2024-06-12",
            "assigned_employee": self.employee.pk
        }
        response = self.client.post('/tasks/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.all().exists())

    def test_list_tasks(self):
        """ Тестирование вывода списка задач """

        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['name'], 'Develop Login Page')

    def test_read_task(self):
        """ Тестирование просмотра задачи """

        response = self.client.get(reverse('tasks:task-read-update-delete', kwargs={'pk': self.first_task.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Develop Login Page')
        self.assertEqual(response.data['priority'], 'medium')

    def test_update_task(self):
        """ Тестирование обновление задачи """

        updated_data = {
            "priority": "high"
        }
        response = self.client.patch(reverse('tasks:task-read-update-delete', kwargs={'pk': self.third_task.id}),
                                     data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['priority'], updated_data['priority'])

    def test_delete_task(self):
        """ Тестирование удаление задачи """

        response = self.client.delete(reverse('tasks:task-read-update-delete', kwargs={'pk': self.first_task.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.first_task.id)


class ImportantTasksViewTest(APITestCase):
    def setUp(self):
        # Создание двух сотрудников
        self.employee1 = Employee.objects.create(first_name="John", last_name="Doe", position="Developer", experience=5)
        self.employee2 = Employee.objects.create(first_name="Jane", last_name="Smith", position="Manager", experience=8)

        # Создание зависимых задач
        self.dependent_task1 = Task.objects.create(name="Dependent Task 1", assigned_employee=self.employee1, deadline=datetime.date.today(), status='in_progress')
        self.dependent_task2 = Task.objects.create(name="Dependent Task 2", assigned_employee=self.employee2, deadline=datetime.date.today(), status='in_progress')

        # Создание задачи, которую нужно назначить
        self.task_to_assign = Task.objects.create(name="Task to Assign", deadline=datetime.date.today(), status='to_assign')

        # Установка связи с dependent_task1
        self.task_to_assign.linked_task.set([self.dependent_task1])

    def test_get_important_tasks(self):
        # Делаем GET-запрос к представлению
        response = self.client.get(reverse('tasks:important_tasks'))

        # Проверяем, что статус ответа 200 OK
        self.assertEqual(response.status_code, 200)

        # Проверяем, что в ответе содержится список задач
        self.assertIsInstance(response.data, list)

        # Проверяем, что в списке задач есть задача, которую нужно назначить
        task_assigned = next((task for task in response.data if task['task'] == 'Task to Assign'), None)
        self.assertIsNotNone(task_assigned)

        # Проверяем, что задача назначена одному из сотрудников
        self.assertIn('employee', task_assigned)
        self.assertIn('fullname', task_assigned['employee'])
        self.assertIn('Doe John', task_assigned['employee']['fullname'])
