from django.urls import path
from .views import runs_view, run_view

app_name = 'runs'

urlpatterns = [
    path('', runs_view, name='main-runs-view'),
    path('run/', run_view, name='main-run-view')
]
