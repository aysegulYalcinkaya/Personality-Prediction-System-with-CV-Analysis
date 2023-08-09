from django import forms
from personality_test.models import Question


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
    personality_1=forms.CharField()
    personality_2 = forms.CharField()
    personality_3 = forms.CharField()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'category']