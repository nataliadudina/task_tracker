from django.db.models import Q, Count
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from employees.models import Employee
from tasks.models import Task
from tasks.paginators import TaskPaginator
from tasks.serializers import TaskSerializer, ImportantTaskSerializer


class TaskListApi(generics.ListCreateAPIView):
    """
        API endpoint для списка задач.

        - GET: Получение списка задач.
        - POST: Создание новой задачи.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    pagination_class = TaskPaginator


class TaskDetailApi(generics.RetrieveUpdateDestroyAPIView):
    """
        API endpoint для детальной информации о задаче и её обновления/удаления.

        - GET: Получение детальной информации о конкретной задаче.
        - PUT: Обновление информации о задаче.
        - DELETE: Удаление задачи.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_update(self, serializer):
        data = self.request.data    # Получение текущие данные из запроса
        assigned_employee_id = data.get('assigned_employee')    # Проверка, назначен ли сотрудник

        serializer.save(partial=True)    # обновление только переданных полей

        instance = serializer.instance

        # Изменение статуса задачи при назначении сотрудника
        if assigned_employee_id is not None:
            instance.status = "in_progress"
        # Изменение статуса задачи при снятии сотрудника
        elif assigned_employee_id is None:
            instance.status = "to_assign"
            instance.completion_time = None

        # Изменение статуса задачи при заполнении графы "completion_time"
        if instance.completion_time:
            if instance.completion_time > instance.deadline:
                instance.status = "overdue"
            elif instance.completion_time <= instance.deadline:
                instance.status = "completed"

        instance.save()


class ImportantTasksView(APIView):
    """
    Представление для получения важных задач, которые ещё не назначены сотрудникам,
    но имеют назначенные зависимые задачи, поиск подходящего для её выполнения сотрудника по критериям.
    """

    def get(self, request):
        """
        Обрабатывает GET-запрос и возвращает список важных задач.

        Returns:
            JsonResponse: JSON-ответ со списком важных задач.
        """

        # Получение задач, от которых зависят другие задачи, взятые в работе
        important_tasks = Task.objects.filter(status='to_assign', linked_task__status='in_progress')
        task_list = []

        for task in important_tasks:

            # Поиск наименее загруженного сотрудника
            least_busy_employees = Employee.objects.annotate(
                active_tasks_count=Count('tasks', filter=Q(tasks__status='in_progress'))).order_by(
                'active_tasks_count').first()
            # Поиск сотрудника, выполняющего родительскую задачу
            employee_with_parent_task = Employee.objects.filter(
                tasks__parent_task__isnull=False  # Фильтрация по задачам, у которых есть родительская задача
            ).annotate(
                task_count=Count('tasks')  # Подсчет количества задач у сотрудника
            ).order_by('task_count').first()

            if not least_busy_employees or not employee_with_parent_task:
                return Response({"error": "No suitable employee found."}, status=400)

            # Сравнение количества задач у наименее загруженного сотрудника и у того, кто выполняет родительскую задачу
            if employee_with_parent_task.task_count <= least_busy_employees.active_tasks_count + 2:
                # Если количество задач у сотрудника, выполняющего родительскую задачу, не превышает количество задач
                # у наименее загруженного сотрудника + 2, то этот сотрудник может взять задачу
                suitable_employee = employee_with_parent_task
            else:
                # В противном случае, наименее загруженный сотрудник является наиболее подходящим кандидатом
                suitable_employee = least_busy_employees

            # Назначение задачи выбранному сотруднику
            task.assigned_employee = suitable_employee
            task.save()  # Сохранение изменений в базе данных

            task_list.append(task)

            # Сериализация списка задач
        serializer = ImportantTaskSerializer(task_list, many=True)
        return Response(serializer.data, status=200)
