from django.urls import path
from histograms.views import run_histograms_view, RunHistogramList, import_view, altair_chart_view, LumisectionHistogram1DList, LumisectionHistogram2DList

app_name = "histograms"
urlpatterns = [
    path("run_histograms/", run_histograms_view, name='run-histograms-view'),
    path("runs/import/", import_view, name='import-view'),
    path("runs/altair/", altair_chart_view, name='altair-view'),
    path("runs/list/", RunHistogramList, name="runs_list"),
    path("lumisections_1D/list/",
         LumisectionHistogram1DList,
         name="lumisections_1D_list"),
    path("lumisections_2D/list/",
         LumisectionHistogram2DList,
         name="lumisections_2D_list"),
]
