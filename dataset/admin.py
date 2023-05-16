from django.contrib import admin
from dataset.models import *

admin.site.register(Folder)
# admin.site.register(File)
admin.site.register(RawDataset)
admin.site.register(RawDatasetFile)
admin.site.register(ProcessedDataset)
admin.site.register(ProcessedDatasetFile)
admin.site.register(Annotations)
admin.site.register(AnnotationFile)
