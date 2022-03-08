import django_tables2 as tables
from django.conf import settings
from django.utils.html import format_html
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.forms import HistogramDataFileForm


class HistogramDataFileTable(tables.Table):
    """
    Custom Table to display information and allow control
    of Histogram datafile parsing.
    """
    filepath = tables.Column()
    in_db = tables.Column(empty_values=())

    # filesize = tables.Column()
    # dimensions = tables.Column(accessor="data_dimensionality")
    # era = tables.Column(accessor="data_era")
    # entries_total = tables.Column()
    # granularity = tables.Column()
    # percentage_processed = tables.Column()

    def render_in_db(self, value):
        return format_html(
            f"<img src='{settings.STATIC_URL}/histogram_file_manager/icons/check.svg' alt=''>"
        ) if value else ""

    class Meta:
        #
        # model = HistogramDataFile
        fields = []
