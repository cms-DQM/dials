from django.urls import include, path
from .views import listLumisectionHistos1D, listLumisectionHistos1DAPI


app_name = "lumisection_histos1D"
urlpatterns = [
    path("list/", listLumisectionHistos1D, name="list"),
    path("API/", listLumisectionHistos1DAPI.as_view(), name = "API"),
]
