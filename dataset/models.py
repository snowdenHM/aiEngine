import uuid
from django.db import models
from project.models import Project
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


########### File Management System ############

class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    folder_name = models.CharField(max_length=100, null=True, blank=True)
    folder_path = models.CharField(max_length=1024, null=True, blank=True)
    folders = models.ManyToManyField('self', related_name='subFolders', symmetrical=False, blank=True)  # Many folders -> Many sub-folders
    parents = models.ForeignKey('self', related_name='parentFolders', on_delete=models.CASCADE, null=True, blank=True)  # Many folders -> One parent folder
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.parents:
            return self.parents.folder_name + " " + self.folder_name
        return self.folder_name

def get_upload_path(instance, filename):
    return instance.parent.folder_path + "/" + filename


class File(models.Model):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=256, null=True, blank=True)
    file_path = models.CharField(max_length=1024, blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    file_extension = models.CharField(max_length=10, blank=True, null=True)
    file_upload = models.FileField(upload_to=get_upload_path)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True, null=True)  # link to parent folder

    def __str__(self):
        return self.file_name

    class Meta:
        abstract = True


############# End of File System ##################


############# Dataset #################

class DatasetBaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Dataset(DatasetBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectDataset')
    train_ratio = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    val_ratio = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='dataParentFolder', blank=True)

    def __str__(self):
        return f"Raw Dataset: {self.name}"

    def clean(self):
        total = self.train_ratio + self.val_ratio
        if round(total, 2) != 1:
            raise ValidationError("The Sum of ratios should be exactly 1")

    class Meta:
        verbose_name_plural = 'Raw Dataset'


class ProcessedDataset(DatasetBaseModel):
    SUBSET_CHOICES = (
        ('training', 'Training'),
        ('validation', 'Validation'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, null=True, blank=True)
    subset = models.CharField(max_length=20, choices=SUBSET_CHOICES, null=True, blank=True)
    sample_counts = models.IntegerField(default=0)
    raw_dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='processedData')

    def __str__(self):
        return f"Processed Dataset: {self.name}"

    class Meta:
        verbose_name_plural = 'Processed Dataset'

class DatasetFile(File):
    processed_dataset = models.ForeignKey(ProcessedDataset, on_delete=models.CASCADE, related_name='datasetFile', blank=True)

    def __str__(self):
        return f"Dataset File: {self.file_name}"

    class Meta:
        verbose_name_plural = 'Dataset File'

# class Annotation(DatasetBaseModel):
#     FORMAT_CHOICES = (
#         ('COCO', 'coco'),
#         ('Pascal VOC', 'pascalVoc'),
#         ('YOLO', 'yolo')
#     )
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=256, null=True, blank=True)
#     processed_dataset = models.ForeignKey(ProcessedDataset, on_delete=models.CASCADE, related_name='annotations',
#                                           null=True, blank=True, default=None)
#     format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
#     count = models.IntegerField(default=0)

#     def __str__(self):
#         return f"Annotation: {self.name}"

#     class Meta:
#         verbose_name_plural = 'Annotation'


class AnnotationFile(File):
    processed_dataset = models.ForeignKey(ProcessedDataset, on_delete=models.CASCADE, related_name='annotationFile')

    def __str__(self):
        return f"Annotation File: {self.file_name}"

    class Meta:
        verbose_name_plural = 'Annotation File'


class ConfigFile(File):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="datasetConfigFile")

    def __str__(self):
        return f"Config File: {self.file_name}"

    class Meta:
        verbose_name_plural = 'Configuration File'

