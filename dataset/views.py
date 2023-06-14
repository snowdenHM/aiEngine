from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from dataset.models import ConfigFile
from django.shortcuts import render, redirect
from dataset.forms import DatasetForm
from dataset.models import Dataset, DatasetFile, ProcessedDataset
from dataset.tasks import preprocess_zip_file
from project.models import Project
from aiEngine.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import boto3


def datasetCreate(request, pk):

    project = Project.objects.get(id=pk)

    form = DatasetForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.save()
        image_file = request.FILES.get('compressed_file')
        label_file = request.FILES.get('compressed_annotation_file')
        classes_file = request.FILES.get('classes_config_file')

        train = float(request.POST['train_ratio'])
        val = float(request.POST['val_ratio'])

        data_folder = data.parent_folder.folders.get(folder_name='data')
        data_folders = data_folder.folders.all().order_by('folder_name')

        config = ConfigFile(
            dataset=data,
            file_name=classes_file.name,
            file_extension=classes_file.name.split('.')[-1],
            file_path=data_folder.folder_path + "/" + classes_file.name,
            file_size=classes_file.size,
            file_upload=classes_file,
            parent=data_folder
        )
        config.save()

        proportions = [train, val]
        
        preprocess_zip_file([image_file, label_file], proportions, data_folders, data)

    else:
        print(form.errors)

    datasets = Dataset.objects.filter(project=project.id)

    context = {
        "datasets": datasets,
        "project": project
        }
    return render(request, 'pages/project/dataset/datasetTable.html', context)

@csrf_exempt
def datasetDelete(request, pk, data_pk):
    project = Project.objects.get(id=pk)
    dataset = Dataset.objects.get(id=data_pk)
    dataset.delete()
    datasets = Dataset.objects.filter(project=project.id)
    context = {
        "datasets": datasets,
        "project": project
    }
    return render(request, 'pages/project/dataset/datasetTable.html', context)

def getStorageData(request, pk):
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)
    size = 0
    for obj in bucket.objects.all():
        size += obj.size
    bucket_size = int(size)/1000/1024/1024
    print("Storage Used (GB):", bucket_size)
    return redirect('project:project', pk)