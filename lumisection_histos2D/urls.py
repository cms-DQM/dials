from django.urls import path
from .views import listLumisectionHistos2D

app_name = "lumisection_histos2D"

urlpatterns = [
    path("list/", listLumisectionHistos2D, name="list"),
]
