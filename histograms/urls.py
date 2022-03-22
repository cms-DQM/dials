from django.urls import path
from histograms.views import LumisectionHistogram1DList, LumisectionHistogram2DList

app_name = "histograms"
urlpatterns = [
    path("lumisections_1D/",
         LumisectionHistogram1DList,
         name="lumisections_1D_list"),
    path("lumisections_2D/",
         LumisectionHistogram2DList,
         name="lumisections_2D_list"),
]
