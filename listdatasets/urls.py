from django.urls import include, path
from . import views

app_name = "listdatasets"
urlpatterns = [
    path("", views.listdatasets, name="listdatasets"),
]