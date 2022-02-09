from django.urls import include, path
from .views import listLumisectionHistos2D, listLumisectionHistos2DAPI


app_name = "lumisection_histos2D"
urlpatterns = [
    path("listLumisectionHistos2D/", listLumisectionHistos2D, name="listLumisectionHistos2D"),
    path("listLumisectionHistos2DAPI/", listLumisectionHistos2DAPI.as_view(), name = "listLumisectionHistos2DAPI"),
]
