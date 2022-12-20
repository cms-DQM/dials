from django import forms
from histogram_file_manager.models import HistogramDataFile, HistogramDataFileContents


class HistogramDataFileStartParsingForm(forms.Form):
    """
    Form for starting the parsing of a specific data file
    """

    granularity = forms.ChoiceField(
        choices=HistogramDataFileContents.DATAFILE_GRANULARITY_CHOICES
    )
    data_dimensionality = forms.ChoiceField(
        choices=HistogramDataFileContents.HISTOGRAM_DIMENSIONS_CHOICES
    )
    file_format = forms.ChoiceField(choices=HistogramDataFile.DATAFILE_FORMAT_CHOICES)
