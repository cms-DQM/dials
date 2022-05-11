from django.contrib import admin
from .models import Task, Strategy, Prediction

admin.site.register(Task)
admin.site.register(Strategy)
admin.site.register(Prediction)
