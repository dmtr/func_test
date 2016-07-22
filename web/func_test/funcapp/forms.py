import json
from django import forms


class DataSetForm(forms.Form):

    dataset = forms.CharField(max_length=2048)

    def clean_dataset(self):
        j = self.cleaned_data['dataset']
        try:
            json.loads(j)
        except:
            raise forms.ValidationError("JSON is not valid")
        return j
