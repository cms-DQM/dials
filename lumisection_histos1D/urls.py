from django.urls import include, path
from .views import listLumisectionHisto1D

app_name = "lumisection_histos1D"

urlpatterns = [
    path("list/", listLumisectionHisto1D, name="list"),
]
