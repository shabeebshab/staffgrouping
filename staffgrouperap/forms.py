from django import forms

class RawDataForm(forms.Form):
    raw_data = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 10, 'placeholder': 'copying text must start with #id like 1,2,3..'}))