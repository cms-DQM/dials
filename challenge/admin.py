import logging
from django.contrib import admin
from .models import Task, Strategy, Prediction

logger = logging.getLogger(__name__)


@admin.action(description="Trigger pipline on selected Task(s)")
def trigger_pipeline(modeladmin, request, queryset):
    for task in queryset:
        try:
            task.trigger_pipeline()
        except Exception as e:
            logger.error(f"{e} when triggering pipline for Task {task.id}")


class TaskAdmin(admin.ModelAdmin):
    actions = [trigger_pipeline]


admin.site.register(Task, TaskAdmin)
admin.site.register(Strategy)
admin.site.register(Prediction)
