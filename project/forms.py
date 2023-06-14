from django import forms
from project.models import Project


class ProjectForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Project
        fields = '__all__'
