import pandas as pd
import altair as alt
from django.shortcuts import render
from django.http import JsonResponse
from django_tables2 import RequestConfig
from data_taking_objects.models import Run
from histograms.utils import get_altair_chart
from histograms.models import (
    RunHistogram,
    LumisectionHistogram1D,
    LumisectionHistogram2D,
)
from histograms.tables import (
    RunHistogramTable,
    LumisectionHistogram1DTable,
    LumisectionHistogram2DTable,
)
from histograms.api.filters import (
    RunHistogramFilter,
    LumisectionHistogram1DFilter,
    LumisectionHistogram2DFilter,
)


def import_view(request):
    return render(request, "histograms/import.html")


# Could be a duplicate of RunHistogramList...
# Just checking a few things
def run_histograms_view(request):

    error_message = None
    list_of_histograms = None

    list_of_histograms = RunHistogram.objects.all()[:200].values_list('title', flat=True)

    context = {
        "error_message": error_message,
        "list_of_histograms": list_of_histograms,
    }
    
    return render(request, "histograms/run_histograms.html", context)


def run_histograms_plotting_view(request):

    error_message = None
    dataset = None
    variable = None
    chart_type = None
    df = None
    mean = None
    chart = {}

    # objects.all().values() provides a dictionary while objects.all().values_list() provides a tuple
    runs_df = pd.DataFrame(Run.objects.all().values())
    runhistos_df = pd.DataFrame(RunHistogram.objects.all()[:200].values())

    if runhistos_df.shape[0] > 0:
        df = pd.merge(runs_df, runhistos_df, left_on="id", right_on="run_id").drop(
            ["id_x", "id_y", "run_id", "date_x", "date_y"], axis=1
        )

        if request.method == "POST":
            dataset = request.POST["dataset"]
            variable = request.POST["variable"]
            chart_type = request.POST["plot_type"]
            print(
                f"dataset: {dataset} / variable: {variable} / chart_type: {chart_type}"
            )

        # df = df.query('primary_dataset.str.lower()==@dataset & title.str.lower()==@variable')
        # df = df.query('primary_dataset==@dataset & title==@variable')
        mean = df["mean"].to_frame().to_html()

        chart = get_altair_chart(chart_type, df=df)

    else:
        error_message = "No runhistos in the database"

    context = {
        "error_message": error_message,
        "df": df,
        "mean": mean,
        "chart": chart,
    }

    return render(request, "histograms/main_run_histograms.html", context)


def altair_chart_view(request):

    # chart = {}

    runhistos_df = pd.DataFrame(RunHistogram.objects.all()[:200].values())

    if runhistos_df.shape[0] > 0:
        chart_obj = (
            alt.Chart(runhistos_df)
            .mark_bar()
            .encode(
                x="mean",
            )
            .to_json(indent=None)
        )

    else:
        print("No runshistos in the database")

    return JsonResponse(chart_obj)


def RunHistogramList(request):
    """
    View to list the filtered 1D histograms for Runs
    """
    context = {}
    runHistos_list = RunHistogram.objects.all()
    runHistos_filter = RunHistogramFilter(request.GET, queryset=runHistos_list)
    runHistos_table = RunHistogramTable(runHistos_filter.qs[:50])

    RequestConfig(request).configure(runHistos_table)

    context["runHistos_table"] = runHistos_table
    context["filter"] = runHistos_filter
    return render(request, "histograms/listRunHistos1D.html", context)


def LumisectionHistogram1DList(request):
    """
    View to list the filtered 1D histograms for Lumisections
    """
    context = {}
    lumisectionHistos1D_list = LumisectionHistogram1D.objects.all()
    lumisectionHistos1D_filter = LumisectionHistogram1DFilter(
        request.GET, queryset=lumisectionHistos1D_list
    )
    lumisectionHistos1D_table = LumisectionHistogram1DTable(
        lumisectionHistos1D_filter.qs[:50]
    )

    RequestConfig(request).configure(lumisectionHistos1D_table)

    context["lumisectionHistos1D_table"] = lumisectionHistos1D_table
    context["filter"] = lumisectionHistos1D_filter
    return render(request, "histograms/listLumisectionHistos1D.html", context)


def LumisectionHistogram2DList(request):
    """
    View to list the filtered 2D histograms for Lumisections
    """
    context = {}
    lumisectionHistos2D_list = LumisectionHistogram2D.objects.all()
    lumisectionHistos2D_filter = LumisectionHistogram2DFilter(
        request.GET, queryset=lumisectionHistos2D_list
    )
    lumisectionHistos2D_table = LumisectionHistogram2DTable(
        lumisectionHistos2D_filter.qs[:50]
    )

    RequestConfig(request).configure(lumisectionHistos2D_table)

    context["lumisectionHistos2D_table"] = lumisectionHistos2D_table
    context["filter"] = lumisectionHistos2D_filter
    return render(request, "histograms/listLumisectionHistos2D.html", context)
