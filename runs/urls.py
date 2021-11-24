from django.urls import include, path
from rest_framework import routers
from .views import runs_view, run_view, RunViewSet

app_name = 'runs'

#router = routers.DefaultRouter()
#router.register(r'runs', RunViewSet)

urlpatterns = [
    path('',     runs_view,  name='main-runs-view'),
    #path('run/',      run_view,   name='main-run-view'),
    #path('api-url/',  include(router.urls)),
   # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
