from django.db import models
from project.models import Project
from django.core.validators import MaxValueValidator, MinValueValidator
########### File Management System ############


class Folder(models.Model):
    folder_name = models.CharField(max_length=100)
    folder_path = models.CharField(max_length=1024, null=True, blank=True)
    folders = models.ManyToManyField('self', related_name='subFolders', symmetrical=False, blank=True)  # Many folders -> Many sub-folders
    parents = models.ForeignKey('self', related_name='parentFolders', on_delete=models.CASCADE, null=True, blank=True)  # Many folders -> One parent folder
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def get_upload_path(instance, filename):
    return instance.parent.folder_path + "/" + filename


class File(models.Model):
    file_name = models.CharField(max_length=256, null=True, blank=True)
    file_path = models.CharField(max_length=1024, blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    file_extension = models.CharField(max_length=10, blank=True, null=True)
    file_upload = models.FileField(upload_to=get_upload_path)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True, null=True)  # link to parent folder
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


############# End of File System ##################


############# Dataset #################

class DatasetBaseModel(models.Model):
    STATUS_CHOICES = (
        ("Complete", "Complete"),
        ("Incomplete", "Incomplete")
    )

    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        abstract = True


class RawDataset(DatasetBaseModel):
    name = models.CharField(max_length=256)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectDataset')
    train_ratio = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    val_ration = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    test_ratio = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"Raw Dataset: {self.name}"

    class Meta:
        verbose_name_plural = 'Raw Dataset'


class RawDatasetFile(File):
    name = models.CharField(max_length=256, null=True, blank=True)
    raw_dataset = models.ForeignKey(RawDataset, on_delete=models.CASCADE, related_name='rawDataFile')

    def __str__(self):
        return f"Raw Dataset File: {self.name}"

    class Meta:
        verbose_name_plural = 'Raw Dataset File'


class ProcessedDataset(DatasetBaseModel):
    SUBSET_CHOICES = (
        ('Training', 'training'),
        ('Validation', 'validation'),
        ('Testing', 'testing'),
    )

    name = models.CharField(max_length=256, null=True, blank=True)
    subset = models.CharField(max_length=20, choices=SUBSET_CHOICES, null=True, blank=True)
    sample_counts = models.IntegerField(default=0)
    raw_dataset = models.ForeignKey(RawDataset, on_delete=models.CASCADE, related_name='processedData')

    def __str__(self):
        return f"Processed Dataset: {self.name}"

    class Meta:
        verbose_name_plural = 'Processed Dataset'


class ProcessedDatasetFile(File):
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

    name = models.CharField(max_length=256, null=True, blank=True)
    processed_dataset = models.ForeignKey(ProcessedDataset, on_delete=models.CASCADE, related_name='annotations',
                                          null=True, blank=True, default=None)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Annotation: {self.name}"

    class Meta:
        verbose_name_plural = 'Annotation'


class AnnotationFile(File):
    name = models.CharField(max_length=256, null=True, blank=True)
    annotation = models.ForeignKey(Annotations, on_delete=models.CASCADE, related_name='annotationFile')

    def __str__(self):
        return f"Annotation File: {self.name}"

    class Meta:
        verbose_name_plural = 'Annotation File'
