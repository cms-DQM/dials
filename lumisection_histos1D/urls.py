from django.urls import include, path
from .views import listLumisectionHistos1D

app_name = "lumisection_histos1D"

urlpatterns = [
    path("list/", listLumisectionHistos1D, name="list"),
]
