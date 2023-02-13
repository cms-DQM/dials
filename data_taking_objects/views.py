import logging

from django.shortcuts import render, redirect

from rest_framework import viewsets

from data_taking_objects.models import Run, Lumisection
from data_taking_objects.api.serializers import RunSerializer

from histograms.models import LumisectionHistogram1D, LumisectionHistogram2D

from .forms import DiagnosticForm
from visualize_histogram.forms import QuickJumpForm

logger = logging.getLogger(__name__)


def runs_view(request):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """

    if request.method == 'GET':
        form = QuickJumpForm(request.GET)
        if form.is_valid():
            runnr = form.cleaned_data["runnr"]
            lumisection = form.cleaned_data["lumisection"]
            title = form.cleaned_data["title"]
            return redirect("visualize_histogram:visualize_histogram",
                runnr=runnr, 
                lumisection=lumisection, 
                title=title
            )
        else: form = QuickJumpForm()
    else:
        form = QuickJumpForm()

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
        "form": form
    }
    return render(request, "data_taking_objects/runs.html", context)


def run_view(request, run_number):

    error_message = None

    try:
        run = Run.objects.get(run_number=run_number)
        lumisections = Lumisection.objects.filter(run_id=run_number)
        num_lumisections = lumisections.count()

        if run:
            logger.info(f"loading following run: {run}")
        else:
            error_message = f"Run {run_number} is not in the DB"

        context = {
            "error_message": error_message,
            "run": run,
            "runnr": run.run_number,
            "lumisections": lumisections,
            "num_lumisections": num_lumisections
        }
        return render(request, "data_taking_objects/run.html", context)
    except Run.DoesNotExist:
        context = {
            "error_message": f"Run {run_number} is not in the DB",
            "runnr": run_number,
            "num_lumisections": 0
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

    try:
        lumisection = Lumisection.objects.get(
            ls_number=lumi_number, run__run_number=run_number
        )

        hist1d = LumisectionHistogram1D.objects.filter(lumisection=lumisection)
        hist2d = LumisectionHistogram2D.objects.filter(lumisection=lumisection)

        n_hist1d = hist1d.count()
        n_hist2d = hist2d.count()

        if lumisection:
            logger.info(f"loading following lumisection: {lumisection}")
        else:
            error_message = "This lumisection is not in the DB"

        context = {
            "error_message": error_message,
            "runnr": run_number,
            "lumi_number": lumi_number,
            "lumisection": lumisection,
            "hist1d": hist1d,
            "hist2d": hist2d,
            "n_hist1d": n_hist1d,
            "n_hist2d": n_hist2d
        }

        return render(request, "data_taking_objects/lumisection.html", context)
    except Lumisection.DoesNotExist:
        context = {
            "error_message": f"Run {run_number}, lumisection {lumi_number} is not in the DB",
            "runnr": run_number,
            "lumi_number": lumi_number,
            "n_hist1d": 0,
            "n_hist2d": 0
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
