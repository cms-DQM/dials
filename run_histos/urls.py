from django.urls import include, path
from .views import run_histos_view, listRunHistos1D, listRunHistos1DAPI,altair_chart_view, import_view


app_name = "run_histos"
urlpatterns = [
    path('',        run_histos_view,   name='main-runhistos-view'),
    path("list/", listRunHistos1D, name="list"),
    path("API/", listRunHistos1DAPI.as_view(), name = "API"),
    path('import/', import_view,       name='import-view'), 
    path('altair/', altair_chart_view, name='altair-view'),
]
