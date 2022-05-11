from django.urls import path
from challenge.views import (
    create_task_view,
)

app_name = "challenge"

urlpatterns = [
    path("create_task/", create_task_view, name="create-task-view"),
]
