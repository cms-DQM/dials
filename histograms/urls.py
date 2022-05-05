from django.urls import path
from histograms.views import (
    run_histograms_view,
    run_histograms_plots_view,
    run_histogram_time_serie_view,

    altair_chart_view,

    RunHistogramList,
    LumisectionHistogram1DList,
    LumisectionHistogram2DList,
)

app_name = "histograms"

urlpatterns = [
    path("run_histograms/", run_histograms_view, name="run-histograms-view"),
    path("run_histograms_plots/", run_histograms_plots_view, name="run-histograms-plots-view"),
    path("run_histogram_time_serie/<>", run_histogram_time_serie_view, name="run-histogram-time-serie-view"),

    path("runs/altair/", altair_chart_view, name="altair-view"),

    path("runs/list/", RunHistogramList, name="runs_list"),
    path(
        "lumisections_1D/list/", LumisectionHistogram1DList, name="lumisections_1D_list"
    ),
    path(
        "lumisections_2D/list/", LumisectionHistogram2DList, name="lumisections_2D_list"
    ),
]
