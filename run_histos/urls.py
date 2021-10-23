from django.urls import path
from .views import chart_select_view

app_name = 'run_histos'

urlpatterns = [
    path('', chart_select_view, name='main-runhistos-view')
]
