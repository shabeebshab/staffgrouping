from django import forms

class RawDataForm(forms.Form):
    raw_data = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 10, 'placeholder': 'copying text must start with  1,2,3..'}))