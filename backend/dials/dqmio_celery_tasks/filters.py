from django_celery_results.models import TASK_STATE_CHOICES, TaskResult
from django_filters import rest_framework as filters


class CeleryTasksFilters(filters.FilterSet):
    min_date_created = filters.NumberFilter(label="Minimum date created", field_name="date_created", lookup_expr="gte")
    max_date_created = filters.NumberFilter(label="Maximum date created", field_name="date_created", lookup_expr="lte")
    min_date_done = filters.NumberFilter(label="Minimum date done", field_name="date_done", lookup_expr="gte")
    max_date_done = filters.NumberFilter(label="Maximum date done", field_name="date_done", lookup_expr="lte")
    status = filters.MultipleChoiceFilter(
        label="File contents ingestion status",
        field_name="status",
        lookup_expr="exact",
        choices=TASK_STATE_CHOICES,
    )

    class Meta:
        model = TaskResult
        fields = [
            "status",
            "task_name",
            "worker",
            "min_date_created",
            "max_date_created",
            "min_date_done",
            "max_date_done",
        ]
