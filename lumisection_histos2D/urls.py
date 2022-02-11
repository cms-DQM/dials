from django.urls import include, path
from .views import listLumisectionHistos2D, listLumisectionHistos2DAPI


app_name = "lumisection_histos2D"
urlpatterns = [
    path("list/", listLumisectionHistos2D, name="list"),
    path("API/", listLumisectionHistos2DAPI.as_view(), name = "API"),
]
