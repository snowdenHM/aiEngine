from django.contrib import admin
from modelMarketplace.models import ModelSetup, ModelTrainingConfig, ModelHistoryDetails

admin.site.register(ModelSetup)
admin.site.register(ModelTrainingConfig)
admin.site.register(ModelHistoryDetails)
