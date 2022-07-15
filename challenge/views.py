import logging
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from challenge.forms import TaskForm
from challenge.models import Task


logger = logging.getLogger(__name__)

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


class TaskDetailView(DetailView):
    model = Task

    def post(self, request, pk, *args, **kwargs):
        success = False
        msg = ""
        try:
            t = Task.objects.get(id=pk)
            t.trigger_pipeline()
            success = True
            msg = f"Pipeline triggered for Task {pk}"
        except Task.DoesNotExist:
            msg = f"No Task with id {pk} exists!"
            logger.error(msg)
        except Exception as e:
            msg = repr(e)
            logger.error(msg)

        return JsonResponse({"success": success, "message": msg})

