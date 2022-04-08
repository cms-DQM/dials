from django.urls import path
from data_taking_objects.views import runs_view

app_name = 'data_taking_objects'

urlpatterns = [
    path('runs/', runs_view, name='main-runs-view'),
]
