from django.urls import include, path
from . import views

app_name = "run_histos"
urlpatterns = [
    path("listRunHistos1D/", views.listRunHistos1D, name="listRunHistos1D"),
]