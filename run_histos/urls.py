from django.urls import path
from .views import chart_select_view, chart_view_altair

app_name = 'run_histos'

urlpatterns = [
    path('',        chart_select_view, name='main-runhistos-view'),
    path('altair/', chart_view_altair, name='altair-view')
]
