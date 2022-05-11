from django.forms import ModelForm

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["training_runs", "testing_runs", "metadata"]
