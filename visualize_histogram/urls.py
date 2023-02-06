from django.urls import include, path

from . import views

app_name = "visualize_histogram"

urlpatterns = [
    path("", views.visualize_histogram_dummy, name="visualize_histogram_dummy"),
    path("<int:runnr>/<int:lumisection>/<title>", views.visualize_histogram, name="visualize_histogram"),
]