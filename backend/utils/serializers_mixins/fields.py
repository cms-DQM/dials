class FieldsFilterMixin:
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.

    Boilerplate from: https://github.com/sideris/drf-optionalfields
    """

    include_argument = "fields"

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop(self.include_argument, None)
        super().__init__(*args, **kwargs)

        if fields:
            self.__filter_fields(fields)
        else:
            self.__handle_from_query_params()

    def __filter_fields(self, fields):
        allowed = set(fields.split(","))
        existing = set(self.fields.keys())
        to_remove = existing - allowed
        for field_name in to_remove:
            self.fields.pop(field_name)

    def __handle_from_query_params(self):
        try:
            request = self.context["request"]
            if request.method != "GET":
                return
        except (AttributeError, TypeError, KeyError):
            return

        query_params = request.query_params
        fields = query_params.get(self.include_argument)
        if fields:
            self.__filter_fields(fields)
