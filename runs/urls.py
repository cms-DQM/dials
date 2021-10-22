from django.urls import path
from .views import chart_select_view

app_name = 'runs'

urlpatterns = [
    path('', chart_select_view, name='main-runs-view')
]
