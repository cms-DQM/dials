from django.urls import path
from .views import run_histos_view, chart_view_altair

app_name = 'run_histos'

urlpatterns = [
    path('',        run_histos_view, name='main-runhistos-view'),
    path('altair/', chart_view_altair, name='altair-view')
]
