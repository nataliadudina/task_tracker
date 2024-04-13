from django.urls import path

from tasks.apps import TasksConfig
from tasks.views import TaskListApi, TaskDetailApi, ImportantTasksView

app_name = TasksConfig.name

urlpatterns = [
    path('tasks/', TaskListApi.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailApi.as_view(), name='task-read-update-delete'),
    path('tasks/important-tasks/', ImportantTasksView.as_view(), name='important_tasks')
]
