from dataset_index.models import DatasetIndex
from rest_framework import serializers


class DatasetNameMixin(serializers.ModelSerializer):
    DATASET_CONTEXT_KEY = "dataset_dict"
    dataset = serializers.SerializerMethodField("get_dataset")

    def get_dataset(self, obj):
        if self.DATASET_CONTEXT_KEY not in self.context.keys():
            self.context[self.DATASET_CONTEXT_KEY] = {}

        if obj.dataset_id in self.context[self.DATASET_CONTEXT_KEY]:
            return self.context[self.DATASET_CONTEXT_KEY][obj.dataset_id]

        dataset_index = DatasetIndex.objects.using(obj._state.db).get(pk=obj.dataset_id)
        self.context[self.DATASET_CONTEXT_KEY][obj.dataset_id] = dataset_index.dataset
        return dataset_index.dataset
