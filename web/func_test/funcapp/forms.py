import json
from django import forms
from django.forms import widgets


class DataSetForm(forms.Form):

    dataset = forms.CharField(
        max_length=2048,
        widget=widgets.Textarea
    )

    def clean_dataset(self):
        j = self.cleaned_data['dataset']
        try:
            json.loads(j)
        except:
            raise forms.ValidationError("JSON is not valid")
        return j


class StartCalculationForm(forms.Form):

    start = forms.BooleanField(
        initial=1,
        widget=widgets.HiddenInput
    )
