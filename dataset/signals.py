from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from aiEngine.settings import AWS_STORAGE_BUCKET_NAME
from dataset.models import Folder, RawDataset
import boto3

@receiver(pre_save, sender=RawDataset)
def create_parent_folder(sender, instance, **kwargs):
    folder_name = instance.name
    folder_path = folder_name.lower().replace(' ', '')

    folder = Folder(folder_name=folder_name, folder_path=folder_path)
    folder.save()
    instance.parent_folder = folder

    training = Folder(folder_name='training', folder_path=folder_path+"/training", parents=folder)
    validation = Folder(folder_name='validation', folder_path=folder_path+"/validation", parents=folder)
    testing = Folder(folder_name='testing', folder_path=folder_path+"/testing", parents=folder)

    sub_folders = [training, validation, testing]
    Folder.objects.bulk_create(sub_folders)

    for fold in sub_folders:
        folder.folders.add(str(fold.id))
    folder.save()


@receiver(post_delete, sender=RawDataset)
def remove_parent_folder(sender, instance, **kwargs):
    s3 = boto3.resource('s3')
    bucket_name = AWS_STORAGE_BUCKET_NAME
    folder = instance.parent_folder
    folder_name = folder.folder_name.lower().replace(' ', '') + '/'
    s3.Bucket(bucket_name).objects.filter(Prefix=folder_name).delete()
    parent_folder = Folder.objects.get(id=folder.id)
    parent_folder.delete()
