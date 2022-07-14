from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from challenge.forms import TaskForm
from challenge.models import Task

# TODO Check that this is the best option
def create_task_view(request):
    """
    View for creating Task instances from
    list of testing runs and testing lumisections.
    """
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = TaskForm()
        return render(request, "challenge/create_task.html", {"form": form})


class TaskListView(ListView):
    model = Task
