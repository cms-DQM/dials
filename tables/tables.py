import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from listdatasets.models import Dataset


class DatasetTable(tables.Table):
    """
    Simple readonly table listing completed rpoject
    """

    name = tables.Column()
    description = tables.Column()
    storagetype = tables.Column(verbose_name="Storage Type")
    location = tables.Column()
    scripts = tables.Column()
    data_view = tables.Column(verbose_name="Dataset View")
    # comment = tables.Column(verbose_name = "")

    class Meta:
        model = Dataset
        fields = ()
        attrs = {"class": "table table-hover table-bordered table-fixed"}

    def render_data_view(self, value):
        return format_html('<a href="{}">' "View" "</a>", value)

    def render_storagetype(self, value):
        value = value.replace(
            "Postgres", "<div class='storage_postgres'>Postgres</div>"
        )
        value = value.replace("EOS", "<div class='storage_eos'>EOS</div>")
        value = value.replace(
            "External", "<div class='storage_external'>External</div>"
        )
        return mark_safe(value)
