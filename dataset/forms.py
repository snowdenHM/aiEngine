from django import forms
from .models import RawDataset, RawDatasetFile


class RawDatasetForm(forms.ModelForm):

    compressed_file = forms.FileField(required=True)

    class Meta:
        model = RawDataset
        fields = "__all__"


class RawDatasetFileForm(forms.ModelForm):

    class Meta:
        model = RawDatasetFile
        fields = ['raw_dataset', 'file_upload']
        widgets = {
            'file_upload': forms.FileInput()
        }
