import uuid
from django.db import models
from project.models import Project
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
########### File Management System ############


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    folder_name = models.CharField(max_length=100)
    folder_path = models.CharField(max_length=1024, null=True, blank=True)
    folders = models.ManyToManyField('self', related_name='subFolders', symmetrical=False, blank=True)  # Many folders -> Many sub-folders
    parents = models.ForeignKey('self', related_name='parentFolders', on_delete=models.CASCADE, null=True, blank=True)  # Many folders -> One parent folder
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
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

    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RawDataset(DatasetBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    version_id = models.IntegerField(default=0, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectDataset')
    train_ratio = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    val_ratio = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    test_ratio = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='dataParentFolder', blank=True)

    def __str__(self):
        return f"Raw Dataset: {self.name}"

    def clean(self):
        total = self.train_ratio + self.val_ratio + self.test_ratio
        if round(total, 2) != 1:
            raise ValidationError("The Sum of ratios should be exactly 1")

    class Meta:
        verbose_name_plural = 'Raw Dataset'

class RawDatasetFile(File):
    raw_dataset = models.ForeignKey(RawDataset, on_delete=models.CASCADE, related_name='rawDatasetFile', blank=True)

    def __str__(self):
        return f"Raw Dataset File: {self.file_name}"

    class Meta:
        verbose_name_plural = 'Raw Dataset File'


class ProcessedDataset(DatasetBaseModel):
    SUBSET_CHOICES = (
        ('Training', 'training'),
        ('Validation', 'validation'),
        ('Testing', 'testing'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, null=True, blank=True)
    subset = models.CharField(max_length=20, choices=SUBSET_CHOICES, null=True, blank=True)
    sample_counts = models.IntegerField(default=0)
    raw_dataset = models.ForeignKey(RawDataset, on_delete=models.CASCADE, related_name='processedData')

    def __str__(self):
        return f"Processed Dataset: {self.name}"

    class Meta:
        verbose_name_plural = 'Processed Dataset'


class ProcessedDatasetFile(models.Model):
    id = models.IntegerField(primary_key=True, default=0, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    processed_dataset = models.ForeignKey(ProcessedDataset, on_delete=models.CASCADE, related_name='processedDataFile')

    def __str__(self):
        return f"Processed Dataset File: {self.name}"

    class Meta:
        verbose_name_plural = 'Processed Dataset File'


class Annotations(DatasetBaseModel):
    FORMAT_CHOICES = (
        ('COCO', 'coco'),
        ('Pascal VOC', 'pascalVoc'),
        ('YOLO', 'yolo')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, null=True, blank=True)
    processed_dataset = models.ForeignKey(ProcessedDataset, on_delete=models.CASCADE, related_name='annotations',
                                          null=True, blank=True, default=None)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Annotation: {self.name}"

    class Meta:
        verbose_name_plural = 'Annotation'


class AnnotationFile(models.Model):
    id = models.IntegerField(primary_key=True, default=0, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    annotation = models.ForeignKey(Annotations, on_delete=models.CASCADE, related_name='annotationFile')

    def __str__(self):
        return f"Annotation File: {self.name}"

    class Meta:
        verbose_name_plural = 'Annotation File'
