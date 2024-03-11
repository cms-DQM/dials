from datetime import datetime

import django.utils.timezone as timezone
from celery import states
from django_celery_results.models import TaskResult
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


APP_TZ = timezone.get_default_timezone()


class TaskResponseBase:
    def __init__(self, task_id, state, ready):
        self.id = task_id
        self.state = state
        self.ready = ready


class TaskResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    state = serializers.CharField()
    ready = serializers.BooleanField()


class CeleryTasksSerializer(serializers.ModelSerializer):
    elapsed_time = serializers.SerializerMethodField(
        method_name="compute_elapsed_time", required=False, allow_null=True
    )

    class Meta:
        model = TaskResult
        fields = (
            "task_id",
            "status",
            "task_name",
            "worker",
            "date_created",
            "date_done",
            "elapsed_time",
        )
        lookup_field = "task_id"

    @extend_schema_field(serializers.IntegerField)
    def compute_elapsed_time(self, obj) -> int:
        if obj.status == states.PENDING:
            return None
        is_ready = obj.status in states.READY_STATES
        ftime = ftime = obj.date_done if is_ready else timezone.make_aware(datetime.now(), APP_TZ)
        return (ftime - obj.date_created).total_seconds()
