from django.urls import include, path

from . import views
import data_taking_objects.views

app_name = "visualize_histogram"

urlpatterns = [
    path("", data_taking_objects.views.runs_view, name="visualize_histogram_dummy"),
    path("<int:runnr>/", views.redirect_run, name="redirect_run"),
    path("<int:runnr>/<int:lumisection>/", views.redirect_lumisection, name="redirect_lumisection"),
    path("<int:runnr>/<int:lumisection>/<title_sanitised>/", views.visualize_histogram, name="visualize_histogram"),
]