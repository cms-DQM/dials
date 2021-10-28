from django.urls import path
from .views import run_histos_view, import_view, altair_chart_view

app_name = 'run_histos'

urlpatterns = [
    path('',        run_histos_view,   name='main-runhistos-view'),
    path('import/', import_view,       name='import-view'), 
    path('altair/', altair_chart_view, name='altair-view'),
]
