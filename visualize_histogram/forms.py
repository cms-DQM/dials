from django import forms

class QuickJumpForm(forms.Form):
    runnr = forms.IntegerField(
        required=True, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    lumisection = forms.IntegerField(
        required=True, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    title = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )