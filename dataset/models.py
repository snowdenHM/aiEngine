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


def get_upload_path(instance, filename):
    return instance.parent.folder_path + "/" + filename


class File(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
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


# class DatasetRawUpload(DatasetBaseModel):
#     name =


