from django.urls import include, path

from . import views

app_name = "visualize_histogram"

urlpatterns = [
    path("", views.visualize_histogram, name="visualize")
]