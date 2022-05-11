from django import forms


class DiagnosticForm(forms.Form):
    run_number = forms.IntegerField()
    lumisection_number = forms.IntegerField()
