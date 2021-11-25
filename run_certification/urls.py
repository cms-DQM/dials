from django.urls import path
from .views import run_certification_view

app_name = 'run_certification'

urlpatterns = [
    path('', run_certification_view, name='main-runcertification-view'),
]
