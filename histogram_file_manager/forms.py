from django import forms
from .models import HistogramDataFile


class HistogramDataFileForm(forms.ModelForm):
    class Meta:
        model = HistogramDataFile
        fields = '__all__'
