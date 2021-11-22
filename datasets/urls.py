from django.urls import include, path
from . import views

app_name = "datasets"
urlpatterns = [
    path("", views.listdatasets, name="listdatasets"),
]