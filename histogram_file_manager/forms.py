from django import forms
from .models import HistogramDataFile


class FileManagerForm(forms.ModelForm):
    class Meta:
        model = HistogramDataFile
        fields = '__all__'
