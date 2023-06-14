import zipfile
from celery import shared_task
from django.core.files.base import ContentFile
from dataset.models import DatasetFile, ProcessedDataset, AnnotationFile


def create_subsets(lst, proportions):
    if len(proportions) != 2:
        return None

    total_proportions = round(sum(proportions), 2)
    if total_proportions != 1:
        return None

    total_elements = len(lst)
    num_of_subsets = len(proportions)
    num_elements_per_part = [int(p * total_elements / total_proportions) for p in proportions]

    remaining_elements = total_elements - sum(num_elements_per_part)
    for i in range(remaining_elements):
        num_elements_per_part[i % num_of_subsets] += 1

    subsets = []
    start = 0
    for num_elements in num_elements_per_part:
        end = start + num_elements
        subsets.append(lst[start:end])
        start = end

    return subsets

@shared_task
def preprocess_zip_file(files, proportions, data_folders, raw_dataset):

    processedDatasets = []
    parent_folder_name = raw_dataset.parent_folder.folder_name
    
    imagesSubFolders = data_folders[0].folders.all().order_by('folder_name')
    labelsSubFolders = data_folders[1].folders.all().order_by('folder_name')

    with zipfile.ZipFile(files[0], 'r') as z:

        subsets = create_subsets(z.namelist(), proportions)
        for i, subset in enumerate(subsets):
            datasetFileInstances = []
            processedDataset = ProcessedDataset(
                name=parent_folder_name + " " + imagesSubFolders[i].folder_name,
                subset=imagesSubFolders[i].folder_name,
                sample_counts=len(subset),
                raw_dataset=raw_dataset
            )
            processedDataset.save()
            processedDatasets.append(processedDataset)
            for name in subset:
                content = z.read(name)
                content_file = ContentFile(content, name=name)
                
                datasetFile = DatasetFile(
                    processed_dataset=processedDataset,
                    file_name=name,
                    file_extension=name.split('.')[-1],
                    file_path=imagesSubFolders[i].folder_path + "/" + name,
                    file_size=content_file.size,
                    file_upload=content_file,
                    parent=imagesSubFolders[i]
                )
                datasetFileInstances.append(datasetFile)

            DatasetFile.objects.bulk_create(datasetFileInstances)


    with zipfile.ZipFile(files[1], 'r') as z:

        subsets = create_subsets(z.namelist(), proportions)
        for i, subset in enumerate(subsets):
            annotationFileInstances = []
            for name in subset:
                content = z.read(name)
                content_file = ContentFile(content, name=name)
                
                annotationFile = AnnotationFile(
                    processed_dataset=processedDatasets[i],
                    file_name=name,
                    file_extension=name.split('.')[-1],
                    file_path=labelsSubFolders[i].folder_path + "/" + name,
                    file_size=content_file.size,
                    file_upload=content_file,
                    parent=labelsSubFolders[i]
                )
                annotationFileInstances.append(annotationFile)

            AnnotationFile.objects.bulk_create(annotationFileInstances)

