from django.urls import include, path
from .views import run_histos_view, chart_view_altair, listRunHistos1D

app_name = "run_histos"
urlpatterns = [
    path('',        run_histos_view, name='main-runhistos-view'),
    path("listRunHistos1D/", listRunHistos1D, name="listRunHistos1D"),
    path('altair/', chart_view_altair, name='altair-view'),
]
