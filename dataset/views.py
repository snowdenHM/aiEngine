from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.contrib import messages
from dataset.models import Folder, File
from django.shortcuts import render, redirect
from .forms import RawDatasetForm, RawDatasetFileForm
from .models import RawDataset, RawDatasetFile
from project.models import Project
import zipfile
import time

def rawDatasetCreate(request, pk):

    project = Project.objects.get(id=pk)
    datasets = RawDataset.objects.filter(project=project.id)

    form = RawDatasetForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.save(commit=False)
        data.version_id = len(datasets) + 1
        data.save()
        file = request.FILES.get('compressed_file')
        instances = []

        print(data.parent_folder.folders)

        t = time.time()
        with zipfile.ZipFile(file, 'r') as z:

            train = int(float(request.POST['train_ratio']) / len(z.namelist()) * 100)
            val = int(float(request.POST['val_ratio']) / len(z.namelist()) * 100)
            test = int(float(request.POST['test_ratio']) / len(z.namelist()) * 100)

            print(train, val, test, len(z.namelist()))

            for name in z.namelist():
                content = z.read(name)
                content_file = ContentFile(content, name=name)

                rawDatasetFile = RawDatasetFile(
                    raw_dataset=data,
                    file_name=name,
                    file_extension=name.split('.')[-1],
                    file_path=data.parent_folder.folder_path + "/" + name,
                    file_size=content_file.size,
                    file_upload=content_file,
                    parent=data.parent_folder
                )

                instances.append(rawDatasetFile)

        RawDatasetFile.objects.bulk_create(instances)

    else:
        print(form.errors)

    datasets = RawDataset.objects.filter(project=project.id)

    context = {
        "datasets": datasets,
        "project": project
        }
    return render(request, 'pages/project/dataset/datasetTable.html', context)

@csrf_exempt
def datasetDelete(request, pk, data_pk):
    project = Project.objects.get(id=pk)
    dataset = RawDataset.objects.get(id=data_pk)
    dataset.delete()
    datasets = RawDataset.objects.filter(project=project.id)
    context = {
        "datasets": datasets,
        "project": project
    }
    return render(request, 'pages/project/dataset/datasetTable.html', context)
