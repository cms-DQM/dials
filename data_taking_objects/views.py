import logging

from django.shortcuts import render

from rest_framework import viewsets

from data_taking_objects.models import Run, Lumisection
from data_taking_objects.api.serializers import RunSerializer

from .forms import DiagnosticForm

logger = logging.getLogger(__name__)


def runs_view(request):

    error_message = None

    runs = Run.objects.all()
    n_runs = runs.count()

    if n_runs > 0:
        logger.info(f"{n_runs} are being loaded")
    else:
        error_message = "No runs in the database"

    context = {
        "error_message": error_message,
        "runs": runs,
    }
    return render(request, "data_taking_objects/runs.html", context)


def run_view(request, run_number):

    error_message = None

    run = Run.objects.filter(run_number=run_number)

    if run:
        logger.info(f"loading following run: {run}")
    else:
        error_message = "This run is not in the DB"

    context = {
        "error_message": error_message,
        "run": run[0],
    }
    return render(request, "data_taking_objects/run.html", context)


def lumisections_view(request):

    error_message = None

    lumisections = Lumisection.objects.all()
    n_lumisections = lumisections.count()

    if n_lumisections > 0:
        logger.info(f"{n_lumisections} are being loaded")
    else:
        error_message = "No lumisections in the database"

    context = {
        "error_message": error_message,
        "lumisections": lumisections,
    }
    return render(request, "data_taking_objects/lumisections.html", context)


def lumisection_view(request, run_number, lumi_number):

    error_message = None

    lumisection = Lumisection.objects.filter(
        ls_number=lumi_number, run__run_number=run_number
    )

    if lumisection:
        logger.info(f"loading following lumisection: {lumisection}")
    else:
        error_message = "This lumisection is not in the DB"

    context = {
        "error_message": error_message,
        "lumisection": lumisection[0],
    }

    return render(request, "data_taking_objects/lumisection.html", context)


def diagnostic_view(request):

    error_message = None
    form = None
    run_number = None
    lumisection_number = None

    if request.method == "POST":
        form = DiagnosticForm(request.POST)
        if form.is_valid():
            run_number = form.cleaned_data["run_number"]
            lumisection_number = form.cleaned_data["lumisection_number"]
            context = {
                "error_message": error_message,
                "form": form,
                "run_number": run_number,
                "lumisection_number": lumisection_number,
            }
            # print(f"context: {context['run_number']},  {context['lumisection_number']}")
            render(request, "data_taking_objects/diagnostic.html", context)

    else:
        form = DiagnosticForm()

    context = {
        "error_message": error_message,
        "form": form,
        "run_number": run_number,
        "lumisection_number": lumisection_number,
    }

    return render(request, "data_taking_objects/diagnostic.html", context)


# class based view (to be compared to function based view)
class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all().order_by("run_number")
    serializer_class = RunSerializer
