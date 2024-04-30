from dim_mes.models import MEs
from django_filters import rest_framework as filters


class MEsMethods(filters.FilterSet):
    me = filters.CharFilter(method="exact_filter_me")
    me__regex = filters.CharFilter(method="regex_filter_me")

    def exact_filter_me(self, queryset, name, value):
        me_ids: list[int] = list(
            MEs.objects.using(queryset.db).filter(me=value).values_list(MEs.me_id.field.name, flat=True)
        )
        return queryset.filter(me_id__in=me_ids)

    def regex_filter_me(self, queryset, name, value):
        me_ids: list[int] = list(
            MEs.objects.using(queryset.db).filter(me__regex=value).values_list(MEs.me_id.field.name, flat=True)
        )
        return queryset.filter(me_id__in=me_ids)
