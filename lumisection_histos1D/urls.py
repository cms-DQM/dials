from django.urls import include, path
from .views import listLumisectionHistos1D, listLumisectionHistos1DAPI


app_name = "lumisection_histos1D"
urlpatterns = [
    path("listLumisectionHistos1D/", listLumisectionHistos1D, name="listLumisectionHistos1D"),
    path("listLumisectionHistos1DAPI/", listLumisectionHistos1DAPI.as_view(), name = "listLumisectionHistos1DAPI"),
]
