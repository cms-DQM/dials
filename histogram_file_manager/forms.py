from django import forms
from histogram_file_manager.models import HistogramDataFile, HistogramDataFileContents


class HistogramDataFileStartParsingForm(forms.Form):
    """
    Form for starting the parsing of a specific data file
    """

    granularity = forms.ChoiceField(
        choices=HistogramDataFileContents.DATAFILE_GRANULARITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    data_dimensionality = forms.ChoiceField(
        choices=HistogramDataFileContents.HISTOGRAM_DIMENSIONS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    file_format = forms.ChoiceField(
        choices=HistogramDataFile.DATAFILE_FORMAT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
