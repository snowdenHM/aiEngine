from django.db import models

########### File Management System ############


class Folder(models.Model):
    name = models.CharField(max_length=100)
    folder_path = models.CharField(max_length=1024, null=True, blank=True)
    folders = models.ManyToManyField('self', related_name='subFolders', symmetrical=False, blank=True)  # Many folders -> Many sub-folders
    parents = models.ForeignKey('self', related_name='parentFolders', on_delete=models.CASCADE, null=True, blank=True)  # Many folders -> One parent folder
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=256)
    file_path = models.CharField(max_length=1024)
    file_size = models.IntegerField()
    file_extension = models.CharField(max_length=10)
    file_upload = models.FileField(upload_to="files", null=True)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE)  # link to parent folder
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


# class DatasetRawUpload(DatasetBaseModel):
#     name =


