from datetime import datetime

import django.utils.timezone as timezone
from celery import states
from django_celery_results.models import TaskResult
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

APP_TZ = timezone.get_default_timezone()


class TaskResponseBase:
    def __init__(self, id, state, ready):
        self.id = id
        self.state = state
        self.ready = ready


class InspectResponseBase:
    def __init__(self, id, name, queue, worker):
        self.id = id
        self.name = name
        self.queue = queue
        self.worker = worker


class TaskResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    state = serializers.CharField()
    ready = serializers.BooleanField()


class InspectResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    queue = serializers.CharField()
    worker = serializers.CharField()


class CeleryTasksSerializer(serializers.ModelSerializer):
    elapsed_time = serializers.SerializerMethodField(method_name="compute_elapsed_time")

    class Meta:
        model = TaskResult
        fields = ("task_id", "status", "date_created", "date_done", "elapsed_time")
        lookup_field = "task_id"

    @extend_schema_field(serializers.IntegerField)
    def compute_elapsed_time(self, obj) -> int:
        is_ready = obj.status in states.READY_STATES
        ftime = ftime = obj.date_done if is_ready else timezone.make_aware(datetime.now(), APP_TZ)
        return (ftime - obj.date_created).total_seconds()
