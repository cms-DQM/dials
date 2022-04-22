from django.urls import path
from data_taking_objects.views import runs_view, run_view, lumisections_view, lumisection_view

app_name = 'data_taking_objects'

urlpatterns = [
    path('runs/', runs_view, name='runs-view'),
    path('run/<int:run_number>/', run_view, name='run-view'),
    path('lumisections/', lumisections_view, name='lumisections-view'),
    path('lumisection/<int:run_number>/<int:lumi_number>/', lumisection_view, name='lumisection-view'),
]
