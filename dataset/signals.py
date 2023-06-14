from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from aiEngine.settings import AWS_STORAGE_BUCKET_NAME
from dataset.models import Folder, Dataset
import boto3

@receiver(pre_save, sender=Dataset)
def create_parent_folder(sender, instance, **kwargs):
    folder_name = instance.name
    folder_path = folder_name.lower().replace(' ', '')

    # Parent Folder
    folder = Folder(folder_name=folder_name, folder_path=folder_path)
    folder.save()
    instance.parent_folder = folder

    # Dataset Folder
    data = Folder(folder_name='data', folder_path=folder_path+"/data", parents=folder)
    model = Folder(folder_name='model', folder_path=folder_path+"/model", parents=folder)
    Folder.objects.bulk_create([data, model])
    for fold in [data, model]:
        folder.folders.add(str(fold.id))

    # Sub Folders for Dataset
    images = Folder(folder_name='images', folder_path=data.folder_path+"/images", parents=data)
    labels = Folder(folder_name='labels', folder_path=data.folder_path+"/labels", parents=data)

    sub_folders = [images, labels]
    Folder.objects.bulk_create(sub_folders)

    for fold in sub_folders:
        data.folders.add(str(fold.id))


    for data_folder in [images, labels]:
        training = Folder(folder_name='training', folder_path=data_folder.folder_path+"/training", parents=data_folder)
        validation = Folder(folder_name='validation', folder_path=data_folder.folder_path+"/validation", parents=data_folder)
        data_folders = [training, validation]

        Folder.objects.bulk_create(data_folders)
        data_folder.folders.add(str(training.id))
        data_folder.folders.add(str(validation.id))



@receiver(post_delete, sender=Dataset)
def remove_parent_folder(sender, instance, **kwargs):
    # s3 = boto3.resource('s3')
    # bucket_name = AWS_STORAGE_BUCKET_NAME
    folder = instance.parent_folder
    # folder_name = folder.folder_name.lower().replace(' ', '') + '/'
    # s3.Bucket(bucket_name).objects.filter(Prefix=folder_name).delete()
    parent_folder = Folder.objects.get(id=folder.id)
    parent_folder.delete()
