from django import forms
from modelMarketplace.models import ModelSetup, ModelTrainingConfig, ModelHistoryDetails


class ModelSetupForm(forms.ModelForm):

    class Meta:
        model = ModelSetup
        fields = "__all__"


class ModelTrainingConfigForm(forms.ModelForm):

    class Meta:
        model = ModelTrainingConfig
        fields = "__all__"


class ModelHistoryDetailsForm(forms.ModelForm):
    class Meta:
        model = ModelHistoryDetails
        fields = "__all__"
