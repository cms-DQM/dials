from django.urls import path
from data_taking_certification.views import run_certification_view

app_name = 'data_taking_certification'

urlpatterns = [
    path('runs/', run_certification_view, name='main-runcertification-view'),
]
