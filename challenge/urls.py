from django.urls import path
from challenge import views

app_name = "challenge"

urlpatterns = [
    path("create_task/", views.create_task_view, name="create-task-view"),
    path("task_list/", views.TaskListView.as_view(), name="task-list"),
    path("task_detail/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
]
