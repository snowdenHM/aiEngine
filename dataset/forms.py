from django import forms
from .models import Dataset

class DatasetForm(forms.ModelForm):

    compressed_file = forms.FileField(required=True)
    compressed_annotation_file = forms.FileField(required=True)
    classes_config_file = forms.FileField(required=True)
    class Meta:
        model = Dataset
        fields = "__all__"

# class AnnotationForm(forms.ModelForm):

#     compressed_file = forms.FileField(required=True)

#     class Meta:
#         model = Annotation
#         fields = "__all__"
         