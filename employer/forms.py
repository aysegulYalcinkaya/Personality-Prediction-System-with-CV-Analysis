from django import forms


class JobForm(forms.Form):
    id=forms.IntegerField()
    title = forms.CharField()
    company = forms.CharField()
    location = forms.CharField()
    summary = forms.CharField()
    description = forms.CharField()
    requirements = forms.CharField()
    start_date = forms.DateField()
    end_date = forms.DateField()