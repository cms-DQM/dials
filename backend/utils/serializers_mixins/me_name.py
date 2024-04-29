from dim_mes.models import MEs
from rest_framework import serializers


class MENameMixin(serializers.ModelSerializer):
    ME_CONTEXT_KEY = "mes_dict"
    me = serializers.SerializerMethodField("get_me")

    def get_me(self, obj):
        if self.ME_CONTEXT_KEY not in self.context.keys():
            self.context[self.ME_CONTEXT_KEY] = {}

        if obj.me_id in self.context[self.ME_CONTEXT_KEY]:
            return self.context[self.ME_CONTEXT_KEY][obj.me_id]

        me_index = MEs.objects.get(pk=obj.me_id)
        self.context[self.ME_CONTEXT_KEY][obj.me_id] = me_index.me
        return me_index.me
