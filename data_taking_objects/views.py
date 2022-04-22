import pandas as pd
from django.shortcuts import render
from rest_framework import viewsets
from data_taking_objects.models import Run, Lumisection
from data_taking_objects.api.serializers import RunSerializer


def runs_view(request):

    error_message = None
    df = None

    # objects.all().values() provides a dictionary
    # while objects.all().values_list() provides a tuple
    runs_df = pd.DataFrame(Run.objects.all().values())

    if runs_df.shape[0] > 0:
        df = runs_df.drop(["id"], axis=1)  # .to_html()
    else:
        error_message = "No runs in the database"

    context = {
        "error_message": error_message,
        "runs": df,
    }
    return render(request, "data_taking_objects/runs.html", context)


def run_view(request, run_number):

    error_message = None
    run_info = None

    runs_df = pd.DataFrame(Run.objects.all().values())

    if run_number in runs_df.run_number.tolist():
        run_info = runs_df
    else:
        error_message = "This run is not in the DB"

    context = {
        "error_message": error_message,
        "run_number": run_number,
        "run_info": run_info,
    }
    return render(request, "data_taking_objects/run.html", context)


def lumisections_view(request):

    error_message = None
    df = None

    # TODO The following lines should be done on the DB side
    lumisections_df = pd.DataFrame(Lumisection.objects.all().values())
    runs_df = pd.DataFrame(Run.objects.all().values())

    if lumisections_df.shape[0] > 0:
        df = runs_df.merge(lumisections_df, left_on="id", right_on="run_id")[
            ["run_number", "ls_number"]
        ]
        print(df.head())
    else:
        error_message = "No lumisections in the database"

    context = {
        "error_message": error_message,
        "lumisections": df,
    }
    return render(request, "data_taking_objects/lumisections.html", context)


def lumisection_view(request, run_number, lumi_number):

    error_message = None

    context = {
        "error_message": error_message,
        "run_number": run_number,
        "lumi_number": lumi_number,
    }

    return render(request, "data_taking_objects/lumisection.html", context)


# class based view (to be compared to function based view)
class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all().order_by("run_number")
    serializer_class = RunSerializer
