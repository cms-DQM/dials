import django_tables2 as tables
from django.conf import settings
from django.utils.html import format_html
from django.core.exceptions import ObjectDoesNotExist
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.forms import HistogramDataFileForm


class HistogramDataFileTable(tables.Table):
    """
    Custom Table to display information and allow control
    of Histogram datafile parsing.

    The initial concept was to base this on HistogramDataFile, but this
    would limit the table's entries to just the ones stored in the database. 

    Since we want to display *all* the available datafiles in a specific directory,
    this custom Table was created. The "from_filepaths" method checks files
    passsed as an argument one by one, and, if they
    are stored in the DB, it copies the info to the appropriate column.
    """

    filepath = tables.Column()
    # in_db = tables.Column(empty_values=())

    filesize = tables.Column(empty_values=(), verbose_name="Filesize (MB)")
    dimensionality = tables.Column()
    era = tables.Column(accessor="data_era")
    entries_total = tables.Column()
    granularity = tables.Column()
    percentage_processed = tables.Column()

    def render_filesize(self, value):
        return f"{value / 1024 / 1024:.2f}"

    # def render_in_db(self, value):
    #     """
    #     Replace True/False "in_db" boolean with checkmark
    #     """
    #     return format_html(
    #         f"<img src='{settings.STATIC_URL}/histogram_file_manager/icons/check.svg' alt=''>"
    #     ) if value else ""

    @classmethod
    def from_filepaths(cls, filepaths: list):
        """
        Create a HistogramDataFileTable using the passed list of filepaths.
  
        Parameters:
        - filepaths: a list of tuples, as returned from the forms.FilePathField class

        """
        # Get all histograms stored in db
        files_in_db = HistogramDataFile.objects.all()

        # Ignore some fields from the HistogramDataFile model
        overridden_fields = ['filepath', 'pk']

        # Data that will be returned to be rendered as a table
        new_table_data = []

        # For each filepath passed as argument
        for f in filepaths:
            new_table_entry = {'filepath': f[0]}
            # If this succeeds, the filepath has already been recorded in db
            try:
                entry = files_in_db.get(filepath=f[0])
                # Copy the values from each fields to the new table entry
                for field in HistogramDataFile._meta.local_fields:
                    if field.name not in overridden_fields:
                        new_table_entry[field.name] = getattr(
                            entry, field.name)
                # Do the same for properties
                for prop in HistogramDataFile._meta._property_names:
                    if prop not in overridden_fields:
                        new_table_entry[prop] = getattr(entry, prop)

                new_table_entry['in_db'] = True

            # File not stored in db, display empty data
            except ObjectDoesNotExist as e:
                new_table_entry['in_db'] = False

            new_table_data.append(new_table_entry)

        # Cross-check if the passed filepaths are stored into the
        # database, and fill the columns with existing data
        return cls(new_table_data)

    class Meta:
        #
        model = HistogramDataFile
        fields = []
