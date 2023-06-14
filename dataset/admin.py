from django.contrib import admin
from dataset.models import *

admin.site.register(Folder)
# admin.site.register(File)
admin.site.register(Dataset)
admin.site.register(DatasetFile)
admin.site.register(ProcessedDataset)
admin.site.register(ConfigFile)
admin.site.register(AnnotationFile)
